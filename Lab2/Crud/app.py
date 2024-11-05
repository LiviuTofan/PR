import sqlite3
import sys
import json
from flask import Flask, request, jsonify
from crud_operations import get_product, create_product, update_product_data, delete_product_data


sys.path.append('/home/liviu/Univer/III year/PR/Lab2')

from Process.read import read_products

app = Flask(__name__)

database = '/home/liviu/Univer/III year/PR/Lab2/Database/products.db'
data = '/home/liviu/Univer/III year/PR/Lab2/Database/products.json'

products, columns, values = read_products(data)

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def fetch_products():
    product_list = []
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    product_id = request.args.get('id', default=None, type=int)
    offset = request.args.get('offset', default=None, type=int)
    limit = request.args.get('limit', default=None, type=int)
    

    # for i in range(1, len(products) + 1):
    #     product = get_product(cursor, i, columns)
    #     print("PRODUCT", i, ":", product)
    #     if product:
    #         product_list.append(product)

    conn.close()

    return jsonify(product_list)

@app.route('/insert/product', methods=['POST'])
def insert_product():
    data = request.json
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    product_id = create_product(cursor, data)
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Product created successfully", "product_id": product_id}), 201


@app.route('/update/product', methods=['PUT'])
def update_product():
    data = request.json
    product_id = request.args.get('id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400
    if not data:
        return jsonify({"error": "No data provided to update"}), 400

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    update_product_data(cursor, product_id, data)

    conn.commit()
    conn.close()

    return jsonify({"message": "Product updated successfully", "product_id": product_id}), 200

@app.route('/delete/product', methods=['DELETE'])
def delete_product():
    product_id = request.args.get('id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    delete_product_data(cursor, product_id)

    conn.commit()
    conn.close()

    return jsonify({"message": "Product deleted successfully", "product_id": product_id}), 200


app.run(debug=True)
