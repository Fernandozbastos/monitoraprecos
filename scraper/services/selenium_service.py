from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import random
import re

logger = logging.getLogger(__name__)

def extract_price_from_text(text):
    """Extrai o preço de um texto usando expressões regulares."""
    price_pattern = r'R\$\s*(\d+[.,]?\d*)'
    match = re.search(price_pattern, text)
    if match:
        price_str = match.group(1).replace('.', '').replace(',', '.')
        try:
            return float(price_str)
        except ValueError:
            return None
    return None

def setup_selenium_driver():
    """Configura e retorna um driver Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Adiciona User-Agent aleatório
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    # Inicializa o driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scrape_price_with_selenium(url, selector=None, timeout=30):
    """Extrai o preço de uma página web usando Selenium com o seletor CSS fornecido."""
    driver = None
    try:
        if not selector:
            logger.warning(f"Seletor CSS não fornecido para URL {url}")
            return None
            
        driver = setup_selenium_driver()
        driver.get(url)
        
        # Espera a página carregar completamente
        time.sleep(random.uniform(3.0, 5.0))
        
        # Usa o seletor CSS fornecido
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            price = extract_price_from_text(element.text)
            if price:
                return price
            else:
                logger.warning(f"Seletor CSS encontrado, mas não foi possível extrair preço do texto: {element.text}")
                return None
        except Exception as e:
            logger.error(f"Erro ao encontrar elemento com seletor {selector}: {str(e)}")
            return None
    
    except Exception as e:
        logger.error(f"Erro ao raspar preço com Selenium da URL {url}: {str(e)}")
        return None
    
    finally:
        if driver:
            driver.quit()