import sqlite3
import json
from flask import Flask, request, jsonify
from free_db import free_database
from create_tables import create_table_product, create_table_other_data
from insert_data import insert_products
from crud import get_product

def main(cursor, columns, values, products):
    #free_database(cursor)
    #create_table_product(cursor)
    #create_table_other_data(cursor, columns, values)
    #insert_products(cursor, products)
    for i in range(len(products)+1):
        product = get_product(cursor, i)
        print("PRODUCT", i, ":", product)

app = Flask(__name__)
@app.route('/products', methods=['GET'])
def fetch_products():
    product_list = []
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    for i in range(1, len(products) + 1):
        product = get_product(cursor, i, columns)
        print("PRODUCT", i, ":", product)
        if product:
            product_list.append(product)

    conn.close()

    return jsonify(product_list)

database = '/home/liviu/Univer/III year/PR/Lab2/Database/products.db'
data = '/home/liviu/Univer/III year/PR/Lab2/Database/products.json'

with open(data, 'r') as file:
    products = json.load(file)

first_product = products[0]
columns = list(first_product['other_data'].keys())
values = list(first_product['other_data'].values())

conn = sqlite3.connect(database)
cursor = conn.cursor()

if __name__ == "__main__":
    app.run(debug=True)

#main(cursor, columns, values, products)
conn.commit()
conn.close()
