import pika
import json
import requests
from queue import Queue

RABBITMQ_QUEUE = "scraper_data"
INSERT_URL = "http://localhost:5000/insert/product"

def connect_to_rabbitmq():
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))

def publish_message(channel, queue_name, message):
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print(f"Published message: {message}")

def consume_rabbitmq(task_queue: Queue):
    """
    Listens to RabbitMQ queue and processes messages.
    """
    def callback(ch, method, properties, body):
        data = json.loads(body)
        try:
            response = requests.post(INSERT_URL, json=data)
            if response.status_code == 201:
                print(f"Data posted successfully: {response.status_code}")
            else:
                print(f"Failed to post data: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error posting data: {e}")
        finally:
            # Notify task queue that one RabbitMQ task is done
            task_queue.put("rabbitmq_task_done")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
    print("Starting RabbitMQ consumer...")
    channel.start_consuming()