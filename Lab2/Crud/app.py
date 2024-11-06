import sqlite3
import sys
import json
from flask import Flask, request, jsonify
from crud_operations import get_product, get_products_with_pagination, create_product, update_product_data, delete_product_data

sys.path.append('/home/liviu/Univer/III year/PR/Lab2')

from Process.read import read_products

app = Flask(__name__)

database = '/home/liviu/Univer/III year/PR/Lab2/Database/products.db'
data = '/home/liviu/Univer/III year/PR/Lab2/Database/products.json'

products, columns, values = read_products(data)

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def fetch_product():
    product_list = []
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=5, type=int)
    product_id = request.args.get('id', default=None, type=int) 

    if product_id is not None:
        # Fetch a single product by ID example: /products?id=1
        product = get_product(cursor, product_id, columns)
        print("PRODUCT", product_id, ":", product)
        if product:
            product_list.append(product)
        conn.close()
        return jsonify(product_list)

    else:
        # Fetch products with pagination example: /products?offset=5&limit=5
        product_list, total_count = get_products_with_pagination(cursor, columns, offset, limit)
        conn.close()
        return jsonify({
            "total_count": total_count,
            "offset": offset,
            "limit": limit,
            "products": product_list
        })

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
