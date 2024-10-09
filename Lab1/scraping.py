import requests
from bs4 import BeautifulSoup

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
    div = content.find('div', class_='category-prods xlists')
    anchor_tags = div.find_all('a', class_='img-wrap')
    for anchor_tag in anchor_tags:
        product_href = anchor_tag.get('href')
        img = anchor_tag.find('img')

def parse_url(url):
    request = get_page(url)
    if request.status_code != 200:
        print("Request failed")
    else:
        print("Response Status:", request.status_code)
        print("------------------")
        content = get_content(request)
        return content


def main(url):
    content = parse_url(url)
    parsed_content = parse_main_page(content)
    user_href = user_choice(parsed_content)

    content = parse_url(user_href)
    category_scraping(content)

url = "https://xstore.md/"
main(url)