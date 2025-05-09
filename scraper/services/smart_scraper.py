"""
Serviço inteligente para extração de preços que testa diferentes métodos e seletores.
Combina Playwright, BeautifulSoup e Selenium para obter o melhor resultado.
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

from scraper.services.playwright_service import scrape_price_with_playwright
from scraper.services.price_scraper import scrape_price
from scraper.services.selenium_service import scrape_price_with_selenium
from scraper.selectors.site_selectors import get_selectors_for_url

logger = logging.getLogger(__name__)

# Configurações
MAX_WORKERS = 2  # Número máximo de workers executando em paralelo
TIMEOUT = 60     # Timeout em segundos para cada método

class ScraperMethod:
    """Enum para os diferentes métodos de scraping"""
    PLAYWRIGHT = "playwright"
    SELENIUM = "selenium"
    BEAUTIFULSOUP = "beautifulsoup"

def smart_price_extraction(url, selector=None, parallel=False, methods=None, timeout=TIMEOUT):
    """
    Extrai o preço usando vários métodos e seletores inteligentemente.
    
    Args:
        url (str): URL do produto
        selector (str, optional): Seletor CSS personalizado
        parallel (bool): Se deve executar métodos em paralelo ou sequencial
        methods (list): Lista de métodos para usar (padrão: todos)
        timeout (int): Timeout em segundos para cada método
        
    Returns:
        dict: Resultado com o preço extraído e informações sobre o método e seletor
    """
    # Obter lista de seletores para o domínio
    selectors = get_selectors_for_url(url, selector)
    logger.info(f"Tentando com {len(selectors)} seletores para {url}")
    
    # Define quais métodos usar (padrão: todos)
    if methods is None:
        methods = [ScraperMethod.PLAYWRIGHT, ScraperMethod.BEAUTIFULSOUP, ScraperMethod.SELENIUM]
    
    # Configuração para execução
    if parallel:
        return _extract_parallel(url, selectors, methods, timeout)
    else:
        return _extract_sequential(url, selectors, methods, timeout)

def _extract_sequential(url, selectors, methods, timeout):
    """Extrai preço sequencialmente, testando cada método e seletor"""
    start_time = time.time()
    results = []
    
    # Para cada método de scraping
    for method in methods:
        method_start_time = time.time()
        
        # Para cada seletor na lista
        for selector in selectors:
            selector_start_time = time.time()
            logger.info(f"Tentando extrair com método {method} e seletor '{selector}'")
            
            price = None
            try:
                if method == ScraperMethod.PLAYWRIGHT:
                    price = scrape_price_with_playwright(url, selector, timeout=timeout*1000)
                elif method == ScraperMethod.BEAUTIFULSOUP:
                    price = scrape_price(url, selector)
                elif method == ScraperMethod.SELENIUM:
                    price = scrape_price_with_selenium(url, selector, timeout=timeout)
            except Exception as e:
                logger.warning(f"Erro ao usar {method} com seletor '{selector}': {str(e)}")
                continue
                
            selector_elapsed = time.time() - selector_start_time
            
            if price:
                success_result = {
                    "success": True,
                    "price": price,
                    "method": method,
                    "selector": selector,
                    "elapsed": selector_elapsed
                }
                logger.info(f"Sucesso! Preço R$ {price:.2f} encontrado com {method} usando seletor '{selector}' em {selector_elapsed:.2f}s")
                return success_result
                
            logger.debug(f"Falha com {method} e seletor '{selector}' após {selector_elapsed:.2f}s")
        
        method_elapsed = time.time() - method_start_time
        logger.info(f"Método {method} falhou para todos os seletores após {method_elapsed:.2f}s")
    
    total_elapsed = time.time() - start_time
    logger.warning(f"Todos os métodos e seletores falharam após {total_elapsed:.2f}s")
    
    return {
        "success": False,
        "price": None,
        "method": None,
        "selector": None,
        "elapsed": total_elapsed,
        "methods_tried": methods,
        "selectors_tried": selectors
    }

def _extract_parallel(url, selectors, methods, timeout):
    """Extrai preço em paralelo, testando diferentes combinações simultaneamente"""
    start_time = time.time()
    tasks = []
    
    # Define a função para executar em paralelo
    def execute_method(method, selector):
        try:
            task_start = time.time()
            price = None
            
            if method == ScraperMethod.PLAYWRIGHT:
                price = scrape_price_with_playwright(url, selector, timeout=timeout*1000)
            elif method == ScraperMethod.BEAUTIFULSOUP:
                price = scrape_price(url, selector)
            elif method == ScraperMethod.SELENIUM:
                price = scrape_price_with_selenium(url, selector, timeout=timeout)
                
            task_elapsed = time.time() - task_start
            
            if price:
                logger.info(f"Sucesso com {method} e seletor '{selector}': R$ {price:.2f} em {task_elapsed:.2f}s")
                return {
                    "success": True,
                    "price": price,
                    "method": method,
                    "selector": selector,
                    "elapsed": task_elapsed
                }
            else:
                logger.debug(f"Falha com {method} e seletor '{selector}' após {task_elapsed:.2f}s")
                return None
        except Exception as e:
            logger.warning(f"Erro ao usar {method} com seletor '{selector}': {str(e)}")
            return None
    
    # Cria as tarefas para execução em paralelo
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Primeiro tenta com Playwright que é mais rápido para alguns seletores
        playwright_futures = {}
        for selector in selectors[:2]:  # Limita para os 2 primeiros seletores para Playwright
            if ScraperMethod.PLAYWRIGHT in methods:
                future = executor.submit(execute_method, ScraperMethod.PLAYWRIGHT, selector)
                playwright_futures[future] = (ScraperMethod.PLAYWRIGHT, selector)
        
        # Espera pelos resultados do Playwright
        for future in as_completed(playwright_futures):
            method, selector = playwright_futures[future]
            try:
                result = future.result(timeout=timeout)
                if result and result["success"]:
                    return result
            except TimeoutError:
                logger.warning(f"Timeout ao executar {method} com seletor '{selector}'")
        
        # Se Playwright falhar, tenta com os outros métodos
        all_futures = {}
        for method in methods:
            if method != ScraperMethod.PLAYWRIGHT:  # Já testamos Playwright
                for selector in selectors:
                    future = executor.submit(execute_method, method, selector)
                    all_futures[future] = (method, selector)
        
        # Processa os resultados à medida que concluem
        for future in as_completed(all_futures):
            method, selector = all_futures[future]
            try:
                result = future.result(timeout=timeout)
                if result and result["success"]:
                    return result
            except TimeoutError:
                logger.warning(f"Timeout ao executar {method} com seletor '{selector}'")
    
    # Se chegou aqui, nenhum método teve sucesso
    total_elapsed = time.time() - start_time
    logger.warning(f"Todos os métodos e seletores falharam após {total_elapsed:.2f}s")
    
    return {
        "success": False,
        "price": None,
        "method": None,
        "selector": None,
        "elapsed": total_elapsed,
        "methods_tried": methods,
        "selectors_tried": selectors
    }