
from scraper.core.driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time

# nb_clicks = 2 seulement pour un test rapide, mais on peut augmenter le nombre de fois pour récupérer plus d'articles pour la source Le360
def get_article_links(nb_clicks=2):
    
    driver = get_driver()
    driver.get("https://fr.le360.ma/toutes-les-actualites/")
    
    wait = WebDriverWait(driver, 10)
        # Fermer la popup OneSignal si elle apparaît
    try:
        dismiss_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#onesignal-slidedown-dialog button.slidedown-button.secondary"))
        )
        dismiss_btn.click()
        print("Popup OneSignal fermée")
        time.sleep(0.5)
    except TimeoutException:
        print("Pas de popup OneSignal")
        
    for i in range(nb_clicks):
        time.sleep(1.5)
        try:
            load_more_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".results-list-load-more"))
            )
            # Clic JS direct — contourne la navbar fixe et toute autre superposition
            driver.execute_script("arguments[0].click();", load_more_btn)
            print(f"Clic {i+1}/{nb_clicks} effectué")
        except TimeoutException:
            print(f"Bouton introuvable au clic {i+1}, fin du chargement.")
            break

    # Récupère tous les liens
    containers = driver.find_elements(By.CSS_SELECTOR, ".article-list--headline-container")
    
    links = []
    
    for container in containers:
        
        anchors = container.find_elements(By.TAG_NAME, "a")
        if len(anchors) >= 2:
          category = anchors[0].get_attribute("title")
          href = anchors[1].get_attribute("href")
          title = anchors[1].get_attribute("title")
          if href:
            links.append({
                "category": category,
                "title": title,
                "url": href
            })

          
    return links