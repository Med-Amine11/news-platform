# Entrer dans un article et extraire : 
   # Titre
   # Auteur 
   # Date 
   # Contenu 
   # Tags 
   # Categorie 

import requests
from bs4 import BeautifulSoup


def scrape_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # titre
    title_element = soup.select_one("h1.post-title")
    title = title_element.text.strip() if title_element else ""

    # catégorie
    category = ""
    category_items = soup.select("li.breadcrumb-item")
    if len(category_items) > 1:
        category = category_items[1].text.strip()

    # auteur
    author_element = soup.select_one("span.author")
    author = author_element.text.strip() if author_element else ""

    # date
    date_element = soup.select_one("span.date-post")
    date = date_element.text.strip() if date_element else ""

    # tags
    tags_elements = soup.select("a.tag_post_tag")
    tags = [tag.text.strip() for tag in tags_elements]

    # contenu
    paragraphs = soup.select("div.article-content p")
    content = "\n".join([
        p.text.strip()
        for p in paragraphs
        if p.text.strip()
    ])

    return {
        "url": url,
        "title": title,
        "category": category,
        "author": author,
        "date": date,
        "tags": tags,
        "content": content , 
        "source" : "Hespress"
    }