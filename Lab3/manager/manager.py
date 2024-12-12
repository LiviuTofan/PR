from threading import Thread
from queue import Queue
from rabbitMQ.rabbitmq_consumer import consume_rabbitmq
from ftp_manager import fetch_ftp_files

if __name__ == "__main__":
    task_queue = Queue()

    rabbitmq_thread = Thread(target=consume_rabbitmq, args=(task_queue,))
    ftp_thread = Thread(target=fetch_ftp_files, args=(task_queue,))

    rabbitmq_thread.start()
    ftp_thread.start()

    rabbitmq_thread.join()
    ftp_thread.join()
