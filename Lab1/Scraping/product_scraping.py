from functools import reduce
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
from Scraping.request_content import parse_url, fetch_http_content

def get_timestamp():
    local_timezone = timezone(timedelta(hours=3))
    local_timestamp = datetime.now(local_timezone).isoformat()
    return local_timestamp


def product_scraping(product_href, product):
    parsed_url = urlparse(product_href)

    # Extract the host and path
    host = parsed_url.netloc or "xstore.md"  # Fallback in case only a path is provided
    path = parsed_url.path or "/"  # Default to root path if none is provided

    # Fetch content based on user selection
    content = fetch_http_content(host, path)

    #content = parse_url(product_href)
    div_name = content.find('div', class_='top-title')
    if div_name:
        product_name = div_name.find('h1').text.strip()
        product['name'] = product_name
    else:
        product['name'] = 'Unknown'
        print("Warning: 'top-title' div not found for this product.")


    div_price = content.find('div', class_='xp-price')
    # First validation if remove white spaces and 'lei' from price
    price = div_price.text.replace('lei', '').replace(' ', '').strip()
    try:
        price = int(price)
        # Second validation if price is negative
        if price <= 0:
            raise ValueError("Price is not valid")
    except ValueError:
        price = None

    currency = div_price.find('span').text
    product['price'] = price
    product['currency'] = currency

    div_description = content.find('div', class_='x-attribute')
    p_tags = div_description.find_all('p')
    for p_tag in p_tags:
        specification = p_tag.span.text
        value = p_tag.text.replace(specification, '').strip()
        if '"' in value:
            value = value.replace('"', 'inch')
        product[specification] = value
    
    return product


def convert_currency(price, currency):
    EUR = 19.0
    MDL = 0.053
    if currency == 'MDL' or currency == 'lei':
        current_currency = 'EUR'
        return price/EUR , current_currency
    else:
        current_currency = 'MDL'
        return price * MDL, current_currency
    

def process_products(products, min_price, max_price):

    mapped_products = list(map(lambda p: {
        **p, 
        'converted_price': convert_currency(p['price'], p['currency'])[0],
        'current_currency': convert_currency(p['price'], p['currency'])[1]
    }, products))

    filtered_products = list(filter(lambda p: min_price <= p['converted_price'] <= max_price, mapped_products))
        
    total_price = reduce(lambda sum, p: sum + p['converted_price'], filtered_products, 0)

    utc_timestamp = get_timestamp()

    return {
        'timestamp': utc_timestamp,
        'total_price': total_price,
        'products': filtered_products
    }
