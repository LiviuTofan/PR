import sqlite3
import sys
import threading
from flask import Flask, request, jsonify, send_from_directory

sys.path.append('/home/liviu/Univer/III year/PR/Lab2')

from Process.read import read_products
from Chat.Services.handler import start_websocket_server
from Crud.crud_operations import get_product, get_products_with_pagination, create_product, update_product_data, delete_product_data

database = '/home/liviu/Univer/III year/PR/Lab2/Database/products.db'
data = '/home/liviu/Univer/III year/PR/Lab2/Database/products.json'

products, columns, values = read_products(data)

connected_users = set()
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

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    content = file.read().decode('utf-8')
    print("FILE CONTENT:", content)

    return jsonify({"message": "File uploaded successfully"}), 200

# ChatRoom
@app.route("/chat")
def serve_chat():
    return send_from_directory('/home/liviu/Univer/III year/PR/Lab2/Chat/Front', 'chat.html')

@app.route("/style.css")
def serve_css():
    return send_from_directory('/home/liviu/Univer/III year/PR/Lab2/Chat/Front', 'style.css')

@app.route("/script.js")
def serve_js():
    return send_from_directory('/home/liviu/Univer/III year/PR/Lab2/Chat/Front', 'script.js')

def start_http_server():
    app.run(port=5000, debug=True, use_reloader=False) 

# Start the WebSocket server in a separate thread and the HTTP server in the main thread
# This allows the two servers to work independently, each on its own port
websocket_thread = threading.Thread(target=start_websocket_server, daemon=True)
websocket_thread.start()

start_http_server()