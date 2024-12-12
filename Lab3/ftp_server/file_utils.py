import os
import json
from ftplib import FTP

FTP_HOST = "127.0.0.1"
FTP_USER = "liviu"
FTP_PASS = "pass"
FTP_DIR = "/"

def write_product_to_file(data, output_dir, counter):
    file_name = os.path.join(output_dir, f"product{counter}.json")
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return file_name

def upload_to_ftp(file_path):
    try:
        with FTP(FTP_HOST) as ftp:
            ftp.login(FTP_USER, FTP_PASS)
            ftp.cwd(FTP_DIR)
            with open(file_path, 'rb') as file:
                ftp.storbinary(f'STOR {os.path.basename(file_path)}', file)
            print(f"Uploaded {file_path} to FTP server.")
    except Exception as e:
        print(f"Error uploading {file_path} to FTP: {e}")
