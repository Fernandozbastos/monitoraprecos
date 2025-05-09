"""
Módulo para gerenciamento de seletores CSS para diferentes sites.
Centraliza a configuração de seletores para facilitar a manutenção.
"""

# Lista de sites comuns e seus seletores CSS para preços
SITE_SELECTORS = {
    # Mercado Livre (Brasil)
    "mercadolivre.com.br": [
        ".ui-pdp-price__second-line .andes-money-amount__fraction",  # Padrão do produto
        ".andes-money-amount__fraction",                             # Alternativa
        "span.price-tag-fraction",                                   # Alternativa antiga
        ".price-tag-amount",                                         # Alternativa
        ".ui-pdp-price span[itemprop='price']"                       # Alternativa com itemprop
    ],
    
    # Amazon (Brasil)
    "amazon.com.br": [
        "span.a-price-whole",                                      # Preço inteiro
        "span.a-offscreen",                                        # Preço oferta
        "#priceblock_ourprice",                                    # Preço normal
        "#priceblock_dealprice",                                   # Preço promocional
        ".a-price .a-offscreen"                                    # Preço alternativo
    ],
    
    # Magazine Luiza
    "magazineluiza.com.br": [
        "p.price-template__text",                                  # Preço principal
        "div.price-template-price-block p.price-template__text",   # Preço alternativo
        ".price-value",                                            # Alternativa
        ".price__value"                                            # Nova alternativa
    ],
    
    # Americanas
    "americanas.com.br": [
        "div.priceSales",                                          # Preço de venda
        "span.price__SalesPrice",                                  # Preço de venda (alternativo)
        ".price__PriceWrapper span",                               # Preço geral
        ".styles__PriceText-sc-x06r9i-0"                           # Nova classe
    ],
    
    # Submarino
    "submarino.com.br": [
        "div.priceSales",                                          # Similar ao Americanas
        "span.price__SalesPrice",
        ".price-info__ListPrice",
        ".styles__PriceText-sc-x06r9i-0"                           # Nova classe (mesma do Americanas)
    ],
    
    # Shopee
    "shopee.com.br": [
        ".pqTWkA",                                                 # Preço principal
        ".DCCoO5",                                                 # Alternativa
        "div.Ybrg9j",                                              # Alternativa 2
        ".product-detail-item .product-details__price"             # Outro seletor
    ],
    
    # Casas Bahia
    "casasbahia.com.br": [
        "span.product-price-value",                                # Preço principal
        ".product-price-value",                                    # Alternativa
        "h4.css-k4s0dn",                                           # Alternativa 2
        ".price__PriceValue"                                       # Nova alternativa
    ],
    
    # Ponto Frio
    "pontofrio.com.br": [
        "span.product-price-value",                                # Similar às Casas Bahia
        ".product-price-value",
        "h4.css-k4s0dn",
        ".price__PriceValue"                                       # Nova alternativa
    ],
    
    # Extra
    "extra.com.br": [
        "span.product-price-value",                                # Similar às Casas Bahia e Ponto Frio
        ".product-price-value",
        "h4.css-k4s0dn",
        ".price__PriceValue"                                       # Nova alternativa
    ],
    
    # Kabum
    "kabum.com.br": [
        "h4.finalPrice",                                           # Preço final
        ".finalPrice",                                             # Alternativa
        "span.priceCard",                                          # Alternativa 2
        ".priceBox__nineCard > span"                               # Nova alternativa
    ],
    
    # Netshoes
    "netshoes.com.br": [
        "div.default-price strong",                                # Preço padrão
        ".default-price strong",                                   # Alternativa
        "span.price-display",                                      # Alternativa 2
        "div.price"                                                # Outra alternativa
    ],
    
    # Genérico - seletores comuns que funcionam na maioria dos sites
    "generic": [
        "[itemprop='price']",                                     # Schema.org markup para preço
        ".price",                                                 # Classe genérica de preço
        ".product-price",                                         # Classe comum para preço de produto
        ".current-price",                                         # Preço atual
        ".sale-price",                                            # Preço de venda/promoção
        ".main-price",                                            # Preço principal
        "*[class*='price']",                                      # Qualquer classe que contenha 'price'
        "*[id*='price']",                                         # Qualquer ID que contenha 'price'
        "*[class*='valor']",                                      # Qualquer classe que contenha 'valor' (pt-BR)
        "*[class*='preco']"                                       # Qualquer classe que contenha 'preco' (pt-BR)
    ]
}

def get_selectors_for_url(url, selector=None):
    """
    Retorna uma lista de seletores CSS para o domínio fornecido
    
    Args:
        url (str): URL do produto
        selector (str, optional): Seletor personalizado que terá prioridade
        
    Returns:
        list: Lista de seletores CSS a serem tentados, em ordem de preferência
    """
    from urllib.parse import urlparse
    
    # Extrair domínio da URL
    domain = urlparse(url).netloc.lower()
    
    # Remover www. se presente
    if domain.startswith('www.'):
        domain = domain[4:]
    
    selectors = []
    
    # Se um seletor personalizado foi fornecido, coloque-o como primeira opção
    if selector:
        selectors.append(selector)
    
    # Verificar se temos seletores para este domínio
    domain_found = False
    for site_domain, domain_selectors in SITE_SELECTORS.items():
        if site_domain in domain:
            selectors.extend([s for s in domain_selectors if s != selector])
            domain_found = True
            break
    
    # Se não encontramos um domínio específico, adicione os seletores genéricos
    if not domain_found:
        selectors.extend(SITE_SELECTORS["generic"])
    
    # Remove duplicatas, preservando a ordem
    unique_selectors = []
    for s in selectors:
        if s not in unique_selectors:
            unique_selectors.append(s)
    
    return unique_selectors

def register_site_selectors(domain, selectors):
    """
    Registra novos seletores para um domínio
    
    Args:
        domain (str): Domínio do site (sem www.)
        selectors (list): Lista de seletores CSS
    """
    if domain in SITE_SELECTORS:
        # Atualiza os seletores existentes
        current_selectors = SITE_SELECTORS[domain]
        # Adiciona novos seletores que não existem
        for selector in selectors:
            if selector not in current_selectors:
                current_selectors.append(selector)
    else:
        # Cria uma nova entrada
        SITE_SELECTORS[domain] = selectors