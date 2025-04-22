from playwright.sync_api import sync_playwright
import logging
import re
import time
import random

logger = logging.getLogger(__name__)

def extract_price_from_text(text):
    """Extrai o preço de um texto usando expressões regulares."""
    # Remove caracteres não numéricos exceto vírgula e ponto
    price_pattern = r'R\$\s*(\d+[.,]?\d*)'
    match = re.search(price_pattern, text)
    if match:
        price_str = match.group(1).replace('.', '').replace(',', '.')
        try:
            return float(price_str)
        except ValueError:
            return None
    return None

def scrape_price_with_playwright(url, selector=None, timeout=30000):
    """
    Extrai o preço de uma página web usando Playwright com o seletor CSS fornecido.
    Playwright é uma alternativa ao Selenium com melhor suporte para ARM.
    """
    if not selector:
        logger.warning(f"Seletor CSS não fornecido para URL {url}")
        return None
        
    try:
        with sync_playwright() as p:
            # Usa o navegador Chromium (funciona em ARM/Apple Silicon)
            browser = p.chromium.launch(headless=True)
            
            # Cria um contexto com User-Agent aleatório
            user_agents = [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
            ]
            
            context = browser.new_context(
                user_agent=random.choice(user_agents),
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = context.new_page()
            
            # Primeiro acessa a página inicial do site
            try:
                domain = url.split('/')[2]
                homepage_url = f"https://{domain}"
                logger.info(f"Acessando página inicial: {homepage_url}")
                page.goto(homepage_url, wait_until="networkidle", timeout=timeout)
                time.sleep(random.uniform(1.0, 3.0))
            except Exception as e:
                logger.warning(f"Erro ao acessar página inicial: {str(e)}. Tentando diretamente a URL do produto.")
            
            # Agora acessa a página do produto
            logger.info(f"Acessando URL do produto: {url}")
            page.goto(url, wait_until="networkidle", timeout=timeout)
            
            # Tenta localizar o elemento com o seletor CSS
            try:
                # Aguarda pelo seletor CSS
                element = page.wait_for_selector(selector, timeout=timeout)
                if element:
                    # Obtém o texto do elemento
                    text = element.text_content()
                    price = extract_price_from_text(text)
                    if price:
                        logger.info(f"Preço encontrado com Playwright: R$ {price}")
                        return price
                    else:
                        logger.warning(f"Seletor CSS encontrado, mas não foi possível extrair preço do texto: {text}")
                else:
                    logger.warning(f"Seletor CSS não encontrado na página: {selector}")
            except Exception as e:
                logger.error(f"Erro ao localizar elemento com seletor {selector}: {str(e)}")
            
            # Captura screenshot para diagnóstico (opcional)
            try:
                screenshot_path = f"/app/logs/screenshot_{int(time.time())}.png"
                page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot salvo em: {screenshot_path}")
            except Exception as e:
                logger.error(f"Erro ao capturar screenshot: {str(e)}")
            
            # Fecha o navegador
            browser.close()
            
            return None
            
    except Exception as e:
        logger.error(f"Erro ao raspar preço com Playwright da URL {url}: {str(e)}")
        return None