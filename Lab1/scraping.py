from product_scraping import product_scraping, process_products
from request_content import parse_url

def parse_main_page(content):
    products = {}
    anchor_tags = content.find_all('a', class_='xcateg')
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

def main(url):
    # Parse main page and see user choice
    content = parse_url(url)
    parsed_content = parse_main_page(content)
    user_href = user_choice(parsed_content)

    # Parse user choice and scrape products, and process them
    content = parse_url(user_href)
    products = category_scraping(content)
    min_price = int(input("Enter min price: "))
    max_price = int(input("Enter max price: "))
    result = process_products(products, min_price, max_price)

    # Extract timestamp, total_price, and filtered products from result
    time_stamp = result['timestamp']
    total_price = result['total_price']
    filtered_products = result['products']

    # Print the results
    print(f"Time: {time_stamp}")
    print(f"Total price: {total_price}")
    print("Filtered products:")
    for product in filtered_products:
        print(product)

url = "https://xstore.md/"
main(url)