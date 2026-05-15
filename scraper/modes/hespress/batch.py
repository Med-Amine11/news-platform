import time 
from scraper.core.hespress.links import get_article_links
from scraper.core.hespress.article import scrape_article
from scraper.utils.storage import load_seen_urls, save_seen_urls
from scraper.messaging.producer import send_batch_event

SEEN_FILE = "scraper/state/hespress/seen_urls.json"

def run_hespress_batch():
    """Lance un cycle de scraping batch Hespress (une seule fois)."""
    seen_urls = set(load_seen_urls(SEEN_FILE))
    links = get_article_links()
    new_articles = []

    for url in links:
        if url not in seen_urls:
            print(f"\nNouvel article détecté : {url}")
            article_data = scrape_article(url)
            seen_urls.add(url)
            new_articles.append(article_data)

    if new_articles:
        for article in new_articles:
            send_batch_event(article)
            seen_urls.add(article["url"])
        save_seen_urls(list(seen_urls), SEEN_FILE)
        print(f"[HESPRESS BATCH] ✓ {len(new_articles)} nouveaux articles envoyés")
    else:
        print("[HESPRESS BATCH] Aucun nouvel article")