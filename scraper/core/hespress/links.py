# Récupérer les URLs des nouveaux articles 

from scraper.core.driver import get_driver
from selenium.webdriver.common.by import By
import time

def get_article_links() : 
    
    driver = get_driver() 
    
    driver.get("https://fr.hespress.com/tag/h24")
    
    # Scroll pour charger plus d'articles
    # max_scroll = 1 juste pour un test rapide on peut augmenter le nombre de fois pour récupérer le maximum des articles en batch
    for _ in range(1):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(1)
    
    # Récupération des liens
    links_elements = driver.find_elements(
        By.CLASS_NAME,
        "stretched-link"
    )
    
    links = []
    
    for element in links_elements:
        
        href = element.get_attribute("href")

        if href :
            links.append(href)
    
    driver.quit()
    
    return links 