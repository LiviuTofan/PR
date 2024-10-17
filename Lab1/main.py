from main_page import parse_main_page
from product_scraping import product_scraping, process_products
from request_content import parse_url, fetch_http_content
from category_scraping import category_scraping
from urllib.parse import urlparse

def user_choice(products):
    for index, (key, value) in enumerate(products.items()):
        print(f"{index + 1}. {key}")
    choice = int(input("Choose a category: "))
    return list(products.values())[choice - 1]

def main(url):
    # Parse main page and see user choice
    #content = parse_url(url)
    content = fetch_http_content("https://xstore.md", "/")
    parsed_content = parse_main_page(content)
    user_href = user_choice(parsed_content)

    # Parse user choice and scrape products, and process them
    #content = parse_url(user_href)
    parsed_url = urlparse(user_href)
    host = parsed_url.netloc or "xstore.md" 
    path = parsed_url.path or "/"

    # Fetch content based on user selection
    content = fetch_http_content(host, path)
    products = category_scraping(content)
    min_price = int(input("Enter min price: "))
    max_price = int(input("Enter max price: "))

    # Extract timestamp, total_price, and filtered products from result
    result = process_products(products, min_price, max_price)
    time_stamp = result['timestamp']
    total_price = result['total_price']
    filtered_products = result['products']

    print(f"Time: {time_stamp}")
    print(f"Total price: {total_price}")
    print("Filtered products:")
    for product in filtered_products:
        print(product)

url = "https://xstore.md/"
main(url)