from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from scraper.services.price_scraper import scrape_price
from scraper.services.playwright_service import scrape_price_with_playwright
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def testar_extrator(request):
    """Endpoint para testar a extração de preços"""
    url = request.data.get('url')
    seletor = request.data.get('seletor')
    
    if not url or not seletor:
        return Response({'detail': 'URL e seletor são obrigatórios'}, status=400)
    
    logger.info(f"Testando extração para URL: {url} com seletor: {seletor}")
    
    # Tenta primeiro com Playwright (mais moderno)
    try:
        preco = scrape_price_with_playwright(url, seletor)
        if preco:
            logger.info(f"Preço extraído com Playwright: {preco}")
            return Response({'preco': preco, 'metodo': 'playwright'})
    except Exception as e:
        logger.error(f"Erro ao extrair preço com Playwright: {str(e)}")
    
    # Se falhar, tenta com o scraper tradicional (BeautifulSoup)
    try:
        preco = scrape_price(url, seletor)
        if preco:
            logger.info(f"Preço extraído com BeautifulSoup: {preco}")
            return Response({'preco': preco, 'metodo': 'beautifulsoup'})
    except Exception as e:
        logger.error(f"Erro ao extrair preço com BeautifulSoup: {str(e)}")
    
    # Se ambos falharem, retorna erro
    return Response({'detail': 'Não foi possível extrair o preço com o seletor fornecido'}, status=400)