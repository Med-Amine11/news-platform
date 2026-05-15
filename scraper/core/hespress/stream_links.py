import requests
from bs4 import BeautifulSoup

def get_latest_links():
    url = "https://fr.hespress.com/tag/h24"
    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers
    )
     
    
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )
    
    links = soup.find_all(
        "a",
        class_="stretched-link"
    )
    
    urls = []

    for link in links:

        href = link.get("href")

        if href:
            urls.append(href)

    return urls
    