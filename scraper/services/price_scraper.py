import requests
from bs4 import BeautifulSoup
import logging
import re
from urllib.parse import urlparse

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

def get_domain(url):
    """Extrai o domínio de uma URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc

def scrape_price(url, selector=None):
    """Extrai o preço de uma página web."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Se tiver um seletor CSS específico, usa ele
        if selector:
            price_element = soup.select_one(selector)
            if price_element:
                return extract_price_from_text(price_element.text)
        
        # Tentativa genérica de encontrar preços
        # Procura por padrões comuns de preço em elementos com classes específicas
        price_classes = [
            '.price', '.product-price', '.current-price', '.sales-price',
            '.offer-price', '.regular-price', '.special-price', '[itemprop="price"]'
        ]
        
        for price_class in price_classes:
            elements = soup.select(price_class)
            for element in elements:
                price = extract_price_from_text(element.text)
                if price:
                    return price
        
        # Se não encontrou, procura no texto da página
        body_text = soup.get_text()
        return extract_price_from_text(body_text)
    
    except Exception as e:
        logger.error(f"Erro ao raspar preço da URL {url}: {str(e)}")
        return None