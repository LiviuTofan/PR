import sqlite3
import json
from flask import Flask, request, jsonify
from free_db import free_database
from create_tables import create_table_product, create_table_other_data
from insert_data import insert_products
from crud import get_product

app = Flask(__name__)

database = '/home/liviu/Univer/III year/PR/Lab2/Database/products.db'
data = '/home/liviu/Univer/III year/PR/Lab2/Database/products.json'

with open(data, 'r') as file:
    products = json.load(file)

@app.route('/products', methods=['GET'])
def fetch_products():
    product_list = []
    
    # Create a new connection for each request
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Assuming products is a list or range with product IDs
    for i in range(1, len(products) + 1):  # Define `products` or update the loop as needed
        product = get_product(cursor, i)
        if product:
            # Convert product (tuple) to a dictionary if needed
            product_dict = {
                "id": product[0],
                "name": product[1],
                "price": product[2],
                # Add other fields based on your schema
            }
            print("Product fetched:", product_dict)
            product_list.append(product_dict)
    
    # Close the database connection
    conn.close()
    
    # Return the product list as a JSON response
    return jsonify(product_list)


app.run(debug=True)
