import pika
import json
import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Lab1')))

from main import main
from Serialization.Product import Product

OUTPUT_DIR = "products"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

file_counter = 1

def write_product_to_file(data, counter):
    file_name = os.path.join(OUTPUT_DIR, f"product{counter}.json")
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Product data written to {file_name}")

# RabbitMQ connection setup
def connect_to_rabbitmq():
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Publish message to RabbitMQ
def publish_message(channel, data):
    if isinstance(data, Product):
        data = data.to_dict()

    # Write the data to a JSON file (this is to upload later on ftp server)
    global file_counter
    write_product_to_file(data, file_counter)
    file_counter += 1

    # Publish the message to RabbitMQ
    message = json.dumps(data)
    channel.basic_publish(exchange='', routing_key='scraper_data', body=message)
    print(f"Message sent: {message}")

# Callback for consuming messages
def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received message: {data}")
    
    url = "http://localhost:5000/insert/product"  # Replace with actual endpoint
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print(f"Posted to webserver: {response.status_code}")
        else:
            print(f"Failed to post: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to webserver: {e}")

# Main script
def main_script():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='scraper_data')

    # Scraping and publishing messages
    url = "https://xstore.md/"
    data = main(url)
    for product in data:
        print(product)
        publish_message(channel, product)
    
    # Close publishing connection
    connection.close()

    # Setup consumer
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.basic_consume(queue='scraper_data', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        connection.close()

if __name__ == "__main__":
    main_script()
