from Scraping.main_page import parse_main_page
from Scraping.product_scraping import product_scraping, process_products
from Scraping.request_content import parse_url, fetch_http_content
from Scraping.category_scraping import category_scraping
from Serialization.Product import Product
from Serialization.json_serelization import custom_json_serialize, custom_json_deserialize
from Serialization.xml_serialization import custom_xml_serialize, custom_xml_deserialize
from Serialization.custom_serialization import liviu_serialization, liviu_deserialization
from urllib.parse import urlparse
import json

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

    product_list = []
    for product_data in filtered_products:
        product = Product(
            href=product_data['href'],
            img=product_data['img'],
            name=product_data['name'],
            converted_price=product_data['converted_price'],
            current_currency=product_data['current_currency'],
            **{k: v for k, v in product_data.items() if k not in ['href', 'img', 'name', 'converted_price', 'current_currency']}
        )
        product_list.append(product)


    # Comment this to work in Lab3 where I don't need serialization
        # json_serialized_product = custom_json_serialize(product)
        # print("Serialized product in JSON:")
        # print(json_serialized_product)
        # products.append(product.to_dict())

    # with open("/home/liviu/Univer/III year/PR/Lab2/Database/products.json", "w") as f:
    #     json.dump(products, f)
    return product_list

url = "https://xstore.md/"
#main(url)