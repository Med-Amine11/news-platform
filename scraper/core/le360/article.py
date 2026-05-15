# Entrer dans un article et extraire : 
   # Auteur 
   # Date 
   # Contenu 
   # Tags 
   
import requests
from bs4 import BeautifulSoup

def scrape_article(url) :
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    # Auteur
    author_tag = soup.find("a", class_="byline-credits-bold href")
    author = author_tag.get_text(strip=True) if author_tag else None

    # Date
    date_tag = soup.find("div", class_="subheadline-date")
    date = date_tag.get_text(strip=True) if date_tag else None

    # Contenu
    article_body = soup.find("article", class_="default__ArticleBody-sc-10mj2vp-2 cvkAGA article-body-wrapper")
    paragraphs = []
    if article_body:
        p_tags = article_body.find_all("p", class_="default__StyledText-sc-10mj2vp-0 CxBBS body-paragraph")
        paragraphs = [p.get_text(strip=True) for p in p_tags]

    # Tags
    tags_holder = soup.find("div", class_="le360-tags-holder")
    tags = []
    if tags_holder:
        tag_links = tags_holder.find_all("a", class_="le360-tags")
        tags = [tag.get_text(strip=True).lstrip("#") for tag in tag_links]

    return {
        "url": url,
        "author": author,
        "date": date,
        "tags": tags,
        "content": paragraphs , 
        "source" : "Le360"
    }


