import requests
from bs4 import BeautifulSoup
import logging
import re
import random
import time
from urllib.parse import urlparse
import hashlib

logger = logging.getLogger(__name__)

# Lista de User-Agents para rotação
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
]

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

def get_request_fingerprint(url):
    """Gera uma impressão digital única para a requisição para evitar duplicatas."""
    return hashlib.md5(url.encode('utf-8')).hexdigest()

def scrape_price(url, selector=None, retries=3):
    """Extrai o preço de uma página web usando APENAS o seletor CSS fornecido."""
    # Se não tiver um seletor CSS específico, retorna None
    if not selector:
        logger.warning(f"Seletor CSS não fornecido para URL {url}")
        return None
        
    # Gera um fingerprint para esta requisição
    request_fp = get_request_fingerprint(url)
    
    for attempt in range(retries):
        try:
            # Adiciona um delay variável para cada tentativa
            time.sleep(random.uniform(3.0, 6.0) * (attempt + 1))
            
            # Rotação de User-Agent
            user_agent = random.choice(USER_AGENTS)
            
            # Cria headers que parecem com um navegador real
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.google.com.br/',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'DNT': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-User': '?1',
                'Sec-CH-UA': '" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
                'Sec-CH-UA-Mobile': '?0'
            }
            
            # Usa uma sessão para manter cookies
            session = requests.Session()
            
            # Primeira faz uma requisição para a página inicial do site
            domain = get_domain(url)
            homepage_url = f"https://{domain}"
            try:
                session.get(homepage_url, headers=headers, timeout=15)
                
                # Espera um pouco antes de acessar a página do produto
                time.sleep(random.uniform(1.0, 3.0))
            except Exception as e:
                logger.warning(f"Erro ao acessar a página inicial {homepage_url}: {str(e)}. Tentando diretamente a URL do produto.")
            
            # Agora acessa a página do produto
            response = session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Usa APENAS o seletor CSS fornecido
            price_element = soup.select_one(selector)
            if price_element:
                price = extract_price_from_text(price_element.text)
                if price:
                    return price
                else:
                    logger.warning(f"Seletor CSS encontrado, mas não foi possível extrair preço do texto: {price_element.text}")
            else:
                logger.warning(f"Seletor CSS não encontrado na página: {selector}")
            
            # Se chegou aqui, não encontrou o preço com o seletor fornecido
            return None
        
        except Exception as e:
            logger.error(f"Erro ao raspar preço da URL {url} (tentativa {attempt+1}/{retries}): {str(e)}")
            if attempt < retries - 1:
                # Espera um pouco antes de tentar novamente, aumentando o tempo a cada tentativa
                delay = random.uniform(5.0, 10.0) * (attempt + 1)
                logger.info(f"Esperando {delay:.2f} segundos antes de tentar novamente...")
                time.sleep(delay)
            else:
                # Última tentativa falhou
                return None
    
    return None