import os
import json
from Lab3.ftp_server.file_utils import write_product_to_file, upload_to_ftp
from rabbitmq_utils import connect_to_rabbitmq, publish_message

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Lab1')))
from main import main
from Serialization.Product import Product

OUTPUT_DIR = "products"
RABBITMQ_QUEUE = "scraper_data"

def process_and_publish(data, channel, counter):
    file_path = write_product_to_file(data, OUTPUT_DIR, counter)
    upload_to_ftp(file_path)
    message = json.dumps(data)
    publish_message(channel, RABBITMQ_QUEUE, message)

def run_scraper():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    data = main("https://xstore.md/")
    for counter, product in enumerate(data, 1):
        if isinstance(product, Product):
            product = product.to_dict()
        process_and_publish(product, channel, counter)
    
    connection.close()

if __name__ == "__main__":
    run_scraper()
