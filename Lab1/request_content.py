import requests
from bs4 import BeautifulSoup
import socket
import ssl

def get_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def parse_url(url):
    request = get_page(url)
    if request.status_code != 200:
        print("Request failed")
    else:
        content = get_content(request)
        return content
    
def get_content(request):
    #soup = BeautifulSoup(request.text, 'html.parser')
    soup = BeautifulSoup(request, 'html.parser')
    return soup

def fetch_http_content(host, path="/"):
    if host.startswith('https://'):
        host = host[len('https://'):]

    # Create a socket for the TCP connection 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Wrap the socket for SSL/TLS because using HTTPS
    ssl_sock = ssl.create_default_context().wrap_socket(sock, server_hostname=host)
    
    # Connect the socket to the server's port (HTTPS uses port 443 by default)
    server_address = (host, 443)
    ssl_sock.connect(server_address)

    try:
        # Send HTTP GET request
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: LiviuTofan\r\nConnection: close\r\n\r\n"
        ssl_sock.sendall(request.encode('utf-8'))

        # Receive the response in chunks
        response = b""
        while True:
            data = ssl_sock.recv(4096)
            if not data:
                break
            response += data

        # Split headers and body
        response_str = response.decode('utf-8')
        headers, body = response_str.split("\r\n\r\n", 1)
        #print("Response headers: \n", headers)

        content = get_content(body)
        return content

    finally:
        ssl_sock.close()
