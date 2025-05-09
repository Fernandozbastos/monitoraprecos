from playwright.sync_api import sync_playwright
import logging
import re
import time
import random
import os

logger = logging.getLogger(__name__)

def extract_price_from_text(text):
    """Extrai o preço de um texto usando expressões regulares."""
    if not text:
        return None
        
    # Primeiro tenta encontrar com o padrão R$
    price_pattern = r'R\$\s*(\d+[.,]?\d*)'
    match = re.search(price_pattern, text)
    
    if match:
        price_str = match.group(1).replace('.', '').replace(',', '.')
        try:
            return float(price_str)
        except ValueError:
            return None
    
    # Se não encontrar com R$, tenta extrair diretamente o número
    price_pattern = r'(\d+[.,]\d+)'
    match = re.search(price_pattern, text)
    if match:
        price_str = match.group(1).replace('.', '').replace(',', '.')
        try:
            return float(price_str)
        except ValueError:
            return None
            
    return None

def scrape_price_with_playwright(url, selector=None, timeout=60000):
    """
    Extrai o preço de uma página web usando Playwright com o seletor CSS fornecido.
    Versão melhorada com estratégias anti-detecção.
    """
    if not selector:
        logger.warning(f"Seletor CSS não fornecido para URL {url}")
        return None
    
    # Criar diretório de logs se não existir
    os.makedirs("/app/logs", exist_ok=True)
        
    try:
        with sync_playwright() as p:
            # Configurações do navegador para evitar detecção
            browser_args = [
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-web-security',
                '--disable-site-isolation-trials',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-infobars',
                '--window-size=1920,1080',
                '--ignore-certificate-errors',
            ]
            
            # Usar o navegador Chromium (funciona em ARM/Apple Silicon)
            browser = p.chromium.launch(
                headless=True,
                args=browser_args
            )
            
            # Lista de User-Agents mais atualizados
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
            ]
            
            selected_user_agent = random.choice(user_agents)
            
            # Criar contexto com configurações avançadas
            context = browser.new_context(
                user_agent=selected_user_agent,
                viewport={'width': 1920, 'height': 1080},
                device_scale_factor=1,
                locale='pt-BR',
                timezone_id='America/Sao_Paulo',
                permissions=['geolocation'],
                java_script_enabled=True,
            )
            
            # Configurações para emular um navegador normal
            context.add_init_script('''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => false,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en-US', 'en'],
                });
            ''')
            
            page = context.new_page()
            
            # Configurar timeout para todas as operações
            page.set_default_timeout(timeout)
            
            # Interceptar requisições para melhorar performance e evitar rastreamento
            intercept_types = ['image', 'media', 'font']
            page.route(
                re.compile('(.*)\.(jpg|jpeg|png|svg|gif|webp|mp4|webm|ogg|mp3|wav|pdf|doc|docx|xls|xlsx|css)$'),
                lambda route: route.abort() if any(t in route.request.resource_type for t in intercept_types) else route.continue_()
            )
            
            try:
                # Alguns sites redirecionam de www para domínio principal ou vice-versa
                parsed_url = url.strip()
                logger.info(f"Acessando URL do produto: {parsed_url}")
                
                # Navegar para a página com opções avançadas
                response = page.goto(
                    parsed_url, 
                    wait_until="domcontentloaded", 
                    timeout=timeout
                )
                
                if not response or response.status >= 400:
                    logger.error(f"Erro ao acessar URL: {parsed_url} - Status code: {response.status if response else 'N/A'}")
                    # Capturar screenshot em caso de erro
                    try:
                        screenshot_path = f"/app/logs/error_status_{int(time.time())}.png"
                        page.screenshot(path=screenshot_path)
                        logger.info(f"Screenshot de erro salvo em: {screenshot_path}")
                    except Exception as es:
                        logger.warning(f"Erro ao capturar screenshot de status: {str(es)}")
                
                # Aguardar um tempo aleatório simulando comportamento humano
                time.sleep(random.uniform(2.0, 4.0))
                
                # Rolar a página para simular comportamento humano
                page.evaluate('''() => {
                    window.scrollTo({
                        top: 300,
                        behavior: 'smooth'
                    });
                }''')
                
                time.sleep(random.uniform(1.0, 2.0))
                
                # Tenta localizar o elemento com o seletor CSS
                try:
                    # Modificar seletor para diferentes sites, se necessário
                    modified_selector = selector
                    if "mercadolivre" in parsed_url:
                        # Tenta vários seletores para o Mercado Livre
                        for ml_selector in [
                            selector,
                            ".ui-pdp-price__second-line .andes-money-amount__fraction",
                            ".andes-money-amount__fraction",
                            "span.price-tag-fraction"
                        ]:
                            logger.info(f"Tentando seletor para ML: {ml_selector}")
                            element = page.query_selector(ml_selector)
                            if element:
                                modified_selector = ml_selector
                                break
                    
                    # Aguarda e verifica se o seletor está disponível
                    element = page.wait_for_selector(modified_selector, timeout=timeout, state="attached")
                    
                    if element:
                        # Obtém o texto do elemento
                        text = element.text_content()
                        logger.info(f"Texto encontrado: '{text}'")
                        
                        price = extract_price_from_text(text)
                        if price:
                            logger.info(f"Preço encontrado com Playwright: R$ {price}")
                            
                            # Captura screenshot para diagnóstico
                            try:
                                screenshot_path = f"/app/logs/success_{int(time.time())}.png"
                                page.screenshot(path=screenshot_path)
                                logger.info(f"Screenshot salvo em: {screenshot_path}")
                            except Exception as es:
                                logger.warning(f"Erro ao capturar screenshot: {str(es)}")
                                
                            # Fecha o navegador
                            browser.close()
                            return price
                        else:
                            logger.warning(f"Seletor CSS encontrado, mas não foi possível extrair preço do texto: '{text}'")
                            
                            # Verificar conteúdo completo do elemento pai
                            parent = page.evaluate('''(selector) => {
                                const el = document.querySelector(selector);
                                return el ? el.parentElement.textContent : null;
                            }''', modified_selector)
                            
                            logger.info(f"Conteúdo do elemento pai: '{parent}'")
                            price_from_parent = extract_price_from_text(parent)
                            if price_from_parent:
                                logger.info(f"Preço encontrado no elemento pai: R$ {price_from_parent}")
                                return price_from_parent
                    else:
                        logger.warning(f"Seletor CSS não encontrado na página: {modified_selector}")
                        
                        # Capturar HTML da página para diagnóstico
                        html_content = page.content()
                        logger.debug(f"HTML da página (primeiros 500 caracteres): {html_content[:500]}...")
                except Exception as e:
                    logger.error(f"Erro ao localizar elemento com seletor {selector}: {str(e)}")
                
                # Captura screenshot da página inteira para diagnóstico
                try:
                    screenshot_path = f"/app/logs/error_{int(time.time())}.png"
                    page.screenshot(path=screenshot_path, full_page=True)
                    logger.info(f"Screenshot salvo em: {screenshot_path}")
                except Exception as e:
                    logger.error(f"Erro ao capturar screenshot: {str(e)}")
                
            except Exception as e:
                logger.error(f"Erro ao navegar para a URL: {str(e)}")
                
                # Capturar screenshot em caso de erro
                try:
                    screenshot_path = f"/app/logs/error_navigate_{int(time.time())}.png"
                    page.screenshot(path=screenshot_path)
                except Exception:
                    pass
            
            # Fecha o navegador
            browser.close()
            return None
            
    except Exception as e:
        logger.error(f"Erro ao raspar preço com Playwright da URL {url}: {str(e)}")
        return None