from django.core.management.base import BaseCommand, CommandError
from core.models import Produto, Plataforma, Dominio
from scraper.tasks import verificar_preco
from scraper.services.price_scraper import scrape_price, get_domain
from scraper.services.playwright_service import scrape_price_with_playwright
import time

class Command(BaseCommand):
    help = 'Testa o scraping de preços para produtos específicos ou todos os produtos'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, help='ID do produto específico para testar', required=False)
        parser.add_argument('--url', type=str, help='URL para testar com um seletor específico', required=False)
        parser.add_argument('--seletor', type=str, help='Seletor CSS para usar com a URL de teste', required=False)
        parser.add_argument('--playwright', action='store_true', help='Força o uso do Playwright')
        parser.add_argument('--async', action='store_true', help='Executa de forma assíncrona usando Celery')
        
    def handle(self, *args, **options):
        produto_id = options.get('id')
        url_teste = options.get('url')
        seletor_teste = options.get('seletor')
        usar_playwright = options.get('playwright')
        executar_async = options.get('async')
        
        # Caso: Testar URL específica com seletor fornecido
        if url_teste and seletor_teste:
            self.stdout.write(self.style.SUCCESS(f'Testando URL: {url_teste} com seletor: {seletor_teste}'))
            
            if usar_playwright:
                preco = scrape_price_with_playwright(url_teste, seletor_teste)
            else:
                preco = scrape_price(url_teste, seletor_teste)
                
            if preco:
                self.stdout.write(self.style.SUCCESS(f'Preço encontrado: R$ {preco:.2f}'))
            else:
                self.stdout.write(self.style.ERROR('Não foi possível extrair o preço'))
                
                if not usar_playwright:
                    self.stdout.write('Tentando com Playwright...')
                    preco = scrape_price_with_playwright(url_teste, seletor_teste)
                    if preco:
                        self.stdout.write(self.style.SUCCESS(f'Preço encontrado com Playwright: R$ {preco:.2f}'))
                    else:
                        self.stdout.write(self.style.ERROR('Não foi possível extrair o preço mesmo com Playwright'))
            
            return
            
        # Caso: Testar produto específico
        if produto_id:
            try:
                produto = Produto.objects.get(id=produto_id)
                self.stdout.write(self.style.SUCCESS(f'Testando produto: {produto.nome} ({produto.url})'))
                
                if executar_async:
                    task = verificar_preco.delay(produto_id)
                    self.stdout.write(self.style.SUCCESS(f'Tarefa agendada com ID: {task.id}'))
                    
                    # Esperar pelo resultado da tarefa
                    self.stdout.write('Aguardando resultado...')
                    for _ in range(30):  # Timeout de 30 segundos
                        time.sleep(1)
                        if task.ready():
                            resultado = task.get()
                            self.stdout.write(self.style.SUCCESS(f'Resultado: {resultado}'))
                            return
                    self.stdout.write(self.style.WARNING('Tempo esgotado. A tarefa ainda está em execução.'))
                    
                else:
                    resultado = verificar_preco(produto_id)
                    self.stdout.write(self.style.SUCCESS(f'Resultado: {resultado}'))
                
            except Produto.DoesNotExist:
                raise CommandError(f'Produto com ID {produto_id} não existe')
                
            return
            
        # Caso: Listar todos os produtos
        produtos = Produto.objects.all()
        if not produtos.exists():
            self.stdout.write(self.style.WARNING('Nenhum produto cadastrado no sistema'))
            return
            
        self.stdout.write(self.style.SUCCESS('Produtos disponíveis para teste:'))
        for produto in produtos:
            self.stdout.write(f'ID: {produto.id} - {produto.nome} - {produto.url}')
            
        self.stdout.write(self.style.SUCCESS('\nPara testar um produto específico, use:'))
        self.stdout.write('python manage.py testar_scraper --id=ID_DO_PRODUTO')
        self.stdout.write('\nPara testar uma URL com seletor específico:')
        self.stdout.write('python manage.py testar_scraper --url=URL --seletor=".classe-preco"')