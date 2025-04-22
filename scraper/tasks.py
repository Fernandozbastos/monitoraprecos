from celery import shared_task
from django.utils import timezone
from core.models import Produto, HistoricoPreco, Plataforma, Dominio
from scraper.services.price_scraper import scrape_price, get_domain
import logging

logger = logging.getLogger(__name__)

@shared_task
def verificar_preco(produto_id):
    """Verifica o preço de um produto e atualiza o histórico."""
    try:
        produto = Produto.objects.get(id=produto_id)
        
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
                pass
        
        # Faz o scraping do preço
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
        raise

@shared_task
def verificar_todos_produtos():
    """Agenda verificação para todos os produtos ativos."""
    produtos = Produto.objects.filter(verificacao_manual=False).order_by('posicao_fila')
    
    for produto in produtos:
        verificar_preco.delay(produto.id)
    
    return f"Agendado verificação para {produtos.count()} produtos"