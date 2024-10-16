import requests
from bs4 import BeautifulSoup

def get_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def parse_url(url):
    request = get_page(url)
    if request.status_code != 200:
        print("Request failed")
    else:
        # print("Response Status:", request.status_code)
        # print("------------------")
        content = get_content(request)
        return content
    
def get_content(request):
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup