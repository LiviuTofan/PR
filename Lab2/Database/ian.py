import sqlite3
import json
from flask import Flask, request, jsonify
from free_db import free_database
from create_tables import create_table_product, create_table_other_data
from insert_data import insert_products
from crud import get_product

def main(cursor, columns, values, products):
    #free_database(cursor)
    create_table_product(cursor)
    create_table_other_data(cursor, columns, values)
    insert_products(cursor, products)
    for i in range(1, len(products)+1):
        product = get_product(cursor, i)
        print("PRODUCT", i, ":", product)


# app = Flask(__name__)
# @app.route('/products', methods=['GET'])
# def fetch_products():
#     product_list = []
#     for i in range(1, len(products) + 1):
#         product = get_product(cursor, i)
#         if product:
#             product_list.append(product)
#     print("Fetched products:", product_list)
#     return jsonify(product_list)


database = '/home/liviu/Univer/III year/PR/Lab2/Database/products.db'
data = '/home/liviu/Univer/III year/PR/Lab2/Database/products.json'

with open(data, 'r') as file:
    products = json.load(file)

first_product = products[0]
keys = list(first_product['other_data'].keys())
values = list(first_product['other_data'].values())

conn = sqlite3.connect(database)
cursor = conn.cursor()

main(cursor, keys, values, products)

# if __name__ == "__main__":
#     app.run(debug=True)
#     main(cursor, keys, values, products, app)