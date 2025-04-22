from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import random
import re
import os

logger = logging.getLogger(__name__)

def extract_price_from_text(text):
    """Extrai o preço de um texto usando expressões regulares."""
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

def scrape_price_with_selenium(url, selector=None, timeout=30):
    """Extrai o preço de uma página web usando Selenium com o seletor CSS fornecido."""
    driver = None
    try:
        if not selector:
            logger.warning(f"Seletor CSS não fornecido para URL {url}")
            return None
            
        # Configura o Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.binary_location = "/usr/bin/google-chrome-stable"
        
        # Adiciona User-Agent aleatório
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        
        # Inicializa o driver do Chrome 
        # Não use o WebDriver Manager, que pode causar o erro -5
        chrome_driver_path = "/usr/bin/chromedriver"
        if os.path.exists(chrome_driver_path):
            driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            
        # Acessa a URL
        logger.info(f"Acessando URL do produto com Selenium: {url}")
        driver.get(url)
        
        # Aguarda um tempo para a página carregar completamente
        time.sleep(5)
        
        # Usa o seletor CSS fornecido
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            
            logger.debug(f"Elemento encontrado com Selenium: {element.text}")
            price = extract_price_from_text(element.text)
            
            if price:
                logger.info(f"Preço encontrado com Selenium: R$ {price}")
                return price
            else:
                logger.warning(f"Seletor CSS encontrado com Selenium, mas não foi possível extrair preço do texto: {element.text}")
                return None
        except Exception as e:
            logger.error(f"Erro ao encontrar elemento com seletor {selector} usando Selenium: {str(e)}")
            return None
    
    except Exception as e:
        logger.error(f"Erro ao raspar preço com Selenium da URL {url}: {str(e)}")
        return None
    
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"Erro ao fechar o driver Selenium: {str(e)}")