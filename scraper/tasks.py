from monitoraprecos.celery import app
from django.utils import timezone
from core.models import Produto, HistoricoPreco, Plataforma, Dominio
from urllib.parse import urlparse
from scraper.services.playwright_service import scrape_price_with_playwright
from scraper.services.price_scraper import scrape_price
from django.db import transaction
import logging
import time
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Tempo de bloqueio (em segundos) para evitar requisições duplicadas
LOCK_TIMEOUT = 60 * 15  # 15 minutos

def get_domain(url):
    """Extrai o domínio de uma URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc

@app.task(bind=True, rate_limit='10/m', max_retries=3)
def verificar_preco(self, produto_id):
    """Verifica o preço de um produto e atualiza o histórico."""
    # Cria um bloqueio para evitar verificações simultâneas do mesmo produto
    lock_id = f"produto_verificando_{produto_id}"
    domain_lock_id = None
    
    # Verifica se já existe um bloqueio para este produto
    if cache.get(lock_id):
        logger.info(f"Produto {produto_id} já está sendo verificado. Pulando...")
        return f"Produto já está sendo verificado"
    
    # Define um bloqueio
    cache.set(lock_id, True, timeout=LOCK_TIMEOUT)
    
    try:
        produto = Produto.objects.get(id=produto_id)
        
        # Se for um produto do cliente, não precisa fazer scraping
        if produto.tipo_produto == 'cliente' and produto.preco_cliente is not None:
            # Apenas registra o preço atual no histórico
            HistoricoPreco.objects.create(
                produto=produto,
                preco=produto.preco_cliente
            )
            
            # Atualiza o timestamp da última verificação
            produto.ultima_verificacao = timezone.now()
            produto.save(update_fields=['ultima_verificacao'])
            
            logger.info(f"Preço do produto do cliente registrado para {produto.nome}: R$ {produto.preco_cliente}")
            return f"Preço do produto do cliente registrado: R$ {produto.preco_cliente}"
        
        # Para produtos de concorrentes, continua com a lógica original
        # Registra início da verificação
        logger.info(f"Iniciando verificação de preço para: {produto.nome} ({produto.url})")
        
        # Determina o seletor CSS a ser usado
        selector = None
        if produto.plataforma and produto.plataforma.seletor_css:
            selector = produto.plataforma.seletor_css
        else:
            # Tenta encontrar um seletor baseado no domínio
            domain = get_domain(produto.url)
            try:
                dominio = Dominio.objects.get(nome__icontains=domain)
                selector = dominio.seletor_css
            except Dominio.DoesNotExist:
                logger.warning(f"Nenhum seletor encontrado para o domínio: {domain}")
                return f"Nenhum seletor CSS definido para o produto {produto.nome}"
        
        # Adiciona um bloqueio por domínio para evitar várias requisições para o mesmo site
        domain_lock_id = f"domain_verificando_{get_domain(produto.url)}"
        
        if cache.get(domain_lock_id):
            # Se o domínio já está sendo acessado, espera um pouco
            logger.info(f"Domínio {get_domain(produto.url)} já está sendo acessado. Esperando...")
            time.sleep(5)  # Espera 5 segundos antes de tentar
        
        # Define um bloqueio para o domínio
        cache.set(domain_lock_id, True, timeout=10)  # Bloqueio de 10 segundos por domínio
        
        # Prioriza Playwright para extração de preço (melhor compatibilidade com ARM/Apple Silicon)
        logger.info(f"Usando Playwright para extrair preço de: {produto.nome}")
        preco = scrape_price_with_playwright(produto.url, selector)
        
        # Se falhar com Playwright, tenta com BeautifulSoup (requests)
        if preco is None:
            logger.info(f"Playwright falhou, tentando com BeautifulSoup para: {produto.nome}")
            preco = scrape_price(produto.url, selector)
        
        if preco:
            # Registra o preço no histórico
            HistoricoPreco.objects.create(
                produto=produto,
                preco=preco
            )
            
            # Atualiza o timestamp da última verificação
            produto.ultima_verificacao = timezone.now()
            produto.save(update_fields=['ultima_verificacao'])
            
            logger.info(f"Preço verificado para {produto.nome}: R$ {preco}")
            return f"Preço verificado para {produto.nome}: R$ {preco}"
        else:
            logger.warning(f"Não foi possível extrair o preço para {produto.nome} ({produto.url})")
            return f"Não foi possível extrair o preço para {produto.nome}"
    
    except Exception as e:
        logger.error(f"Erro ao verificar preço: {str(e)}")
        # Tenta novamente após um tempo
        countdown = 60 * (self.request.retries + 1)  # Aumenta o tempo a cada tentativa
        self.retry(exc=e, countdown=countdown)
        
    finally:
        # Remove os bloqueios quando terminar
        cache.delete(lock_id)
        if domain_lock_id:
            cache.delete(domain_lock_id)

@app.task
def verificar_todos_produtos(tamanho_lote=10, max_produtos=None):
    """
    Agenda verificação para todos os produtos ativos respeitando a fila.
    
    Args:
        tamanho_lote: Número de produtos por lote
        max_produtos: Número máximo de produtos a verificar (None = todos)
    """
    # Obtém produtos ordenados pela posição na fila e pela última verificação
    # Isso garante que produtos há mais tempo sem verificação tenham prioridade
    with transaction.atomic():
        produtos = Produto.objects.filter(
            verificacao_manual=False
        ).order_by(
            'posicao_fila', 
            'ultima_verificacao'
        ).select_for_update()
        
        if max_produtos:
            produtos = produtos[:max_produtos]
        
        produto_ids = list(produtos.values_list('id', flat=True))
    
    total_produtos = len(produto_ids)
    if total_produtos == 0:
        return "Nenhum produto para verificar"
    
    # Agenda cada produto individualmente, respeitando a prioridade da fila
    tarefas = []
    for produto_id in produto_ids:
        tarefa = verificar_preco.delay(produto_id)
        tarefas.append(tarefa.id)
    
    return f"Verificação agendada para {total_produtos} produtos. IDs das tarefas: {tarefas[:5]}..."
    
@app.task
def atualizar_posicoes_fila():
    """
    Atualiza as posições na fila com base em regras de negócio.
    Por exemplo, produtos que foram verificados recentemente vão para o final da fila.
    """
    try:
        with transaction.atomic():
            # Obtém todos os produtos
            produtos = Produto.objects.all().select_for_update()
            
            # Define a ordem: 
            # 1. Produtos nunca verificados
            # 2. Produtos não verificados há muito tempo
            # 3. Produtos verificados recentemente
            ordenados = sorted(
                produtos,
                key=lambda p: (
                    p.ultima_verificacao is not None,  # Primeiro os nunca verificados
                    p.ultima_verificacao or timezone.now()  # Depois por data da última verificação
                )
            )
            
            # Atualiza as posições
            for posicao, produto in enumerate(ordenados):
                if produto.posicao_fila != posicao:
                    produto.posicao_fila = posicao
                    produto.save(update_fields=['posicao_fila'])
        
        return f"Posições na fila atualizadas para {len(ordenados)} produtos"
    except Exception as e:
        logger.error(f"Erro ao atualizar posições na fila: {str(e)}")
        raise
    
@app.task
def testar_conectividade(url_teste="https://www.google.com"):
    """
    Tarefa para testar se o sistema está conseguindo acessar a internet.
    Útil para diagnóstico de problemas de rede.
    """
    try:
        logger.info(f"Testando conectividade com {url_teste}")
        resultado = scrape_price_with_playwright(url_teste, "body")
        if resultado is not None:
            return f"Conectividade OK - conseguiu acessar {url_teste}"
        else:
            return f"Conseguiu acessar {url_teste}, mas não obteve resultado"
    except Exception as e:
        logger.error(f"Erro ao testar conectividade: {str(e)}")
        return f"Erro de conectividade: {str(e)}"