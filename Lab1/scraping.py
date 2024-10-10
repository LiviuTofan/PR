import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

def get_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response
    
def get_content(request):
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def parse_main_page(request):
    products = {}
    anchor_tags = request.find_all('a', class_='xcateg')
    for ancho_tag in anchor_tags:
        href = ancho_tag.get('href')
        span = ancho_tag.find('span')
        category = span.text
        products[category] = href

    return products

def user_choice(products):
    for index, (key, value) in enumerate(products.items()):
        print(f"{index + 1}. {key}")
    choice = int(input("Choose a category: "))
    return list(products.values())[choice - 1]

def category_scraping(content):
    products = []
    div = content.find('div', class_='category-prods xlists')
    anchor_tags = div.find_all('a', class_='img-wrap')
    for anchor_tag in anchor_tags:
        product = {}
        product_href = anchor_tag.get('href')
        img = anchor_tag.find('img').get('src')
        product['href'] = product_href
        product['img'] = img

        product = product_scraping(product_href, product)
        products.append(product)

    return products

def product_scraping(product_href, product):
    content = parse_url(product_href)
    div_name = content.find('div', class_='top-title')
    product_name = div_name.find('h1').text.strip()
    if not product_name:
        raise ValueError("Product name not found")
    product['name'] = product_name

    div_price = content.find('div', class_='xp-price')
    price = div_price.text.replace('lei', '').replace(' ', '').strip()
    try:
        price = int(price)
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
        product[specification] = value
    
    return product



def parse_url(url):
    request = get_page(url)
    if request.status_code != 200:
        print("Request failed")
    else:
        # print("Response Status:", request.status_code)
        # print("------------------")
        content = get_content(request)
        return content
    
def convert_currency(price, currency):
    if currency == 'MDL' or currency == 'lei':
        current_currency = 'EUR'
        return price/EUR , current_currency
    else:
        current_currency = 'MDL'
        return price * MDL, current_currency
    
def get_timestamp():
    local_timezone = timezone(timedelta(hours=3))
    local_timestamp = datetime.now(local_timezone).isoformat()
    return local_timestamp

def process_products(products, min_price, max_price):
    prefered_products = []
    for product in products:
        price = product['price']
        currency = product['currency']
        converted_price, current_currency = convert_currency(price, currency)
        product['converted_price'] = converted_price
        product['current_currency'] = current_currency
        if converted_price >= min_price and converted_price <= max_price:
            prefered_products.append(product)

    utc_timestamp = get_timestamp()
    print("Timestamp:", utc_timestamp)
    return prefered_products

def main(url):
    content = parse_url(url)
    parsed_content = parse_main_page(content)
    user_href = user_choice(parsed_content)

    content = parse_url(user_href)
    products = category_scraping(content)
    min_price = int(input("Enter min price: "))
    max_price = int(input("Enter max price: "))
    result = process_products(products, min_price, max_price)
    print(result)

url = "https://xstore.md/"
EUR = 19.0
MDL = 0.053
main(url)