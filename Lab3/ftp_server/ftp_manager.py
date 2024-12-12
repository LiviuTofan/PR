import os
import time
from ftplib import FTP
import requests
from queue import Queue

FTP_HOST = "127.0.0.1"
FTP_USER = "liviu"
FTP_PASS = "pass"
FTP_DIR = "/"
LOCAL_DOWNLOAD_DIR = "downloads"
UPLOAD_URL = "http://127.0.0.1:5000/upload"

def fetch_ftp_files(task_queue: Queue):
    """
    Periodically fetches files from the FTP server after RabbitMQ tasks are processed.
    """
    os.makedirs(LOCAL_DOWNLOAD_DIR, exist_ok=True)
    file_index = 0  # Index to track which file to fetch next

    while True:
        # Wait for RabbitMQ tasks to be processed
        task_queue.get()

        try:
            with FTP(FTP_HOST) as ftp:
                ftp.login(FTP_USER, FTP_PASS)
                ftp.cwd(FTP_DIR)
                files = ftp.nlst()

                if files:
                    # Use modulo to wrap around if index exceeds file count
                    file_name = files[file_index % len(files)]
                    file_index += 1  # Increment index for the next file

                    local_file_path = os.path.join(LOCAL_DOWNLOAD_DIR, file_name)

                    # Fetch the file from FTP
                    with open(local_file_path, 'wb') as f:
                        ftp.retrbinary(f"RETR {file_name}", f.write)
                    print(f"Fetched {file_name} from FTP.")

                    # Send the file to the upload endpoint
                    with open(local_file_path, 'rb') as file:
                        response = requests.post(UPLOAD_URL, files={"file": file})
                        print(f"Sent {file_name}, response: {response.status_code}")

                    # Delete the local copy after uploading
                    os.remove(local_file_path)
                    print(f"Deleted local file {file_name}.")
                else:
                    print("No files available on FTP server.")

            # Wait 30 seconds before fetching the next file
            time.sleep(30)

        except Exception as e:
            print(f"Error fetching files: {e}")
