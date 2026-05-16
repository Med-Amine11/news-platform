import time 
from scraper.core.hespress.stream_links import get_latest_links
from scraper.core.hespress.article import scrape_article
from scraper.utils.storage import load_seen_urls, save_seen_urls, save_article
from scraper.messaging.producer import send_stream_event

SEEN_FILE = "scraper/state/hespress/seen_urls_stream.json"

def run_hespress_stream():
    """Lance un cycle de scraping stream Hespress (une seule fois)."""
    seen_urls = set(load_seen_urls(SEEN_FILE))
    links = get_latest_links()
    new_articles = []

    for url in links:
        if url not in seen_urls:
            print(f"\nNouvel article détecté : {url}")
            article_data = scrape_article(url)
            new_articles.append(article_data)

    if new_articles:
        for article in new_articles:
            send_stream_event(article)
            seen_urls.add(article["url"])
        save_seen_urls(list(seen_urls), SEEN_FILE)
        print(f"[HESPRESS STREAM] ✓ {len(new_articles)} nouveaux articles envoyés")
    else:
        print("[HESPRESS STREAM] Aucun nouvel article")
