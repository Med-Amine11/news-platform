from scraper.core.le360.links import get_article_links
from scraper.core.le360.article import scrape_article
from scraper.utils.storage import load_seen_urls, save_seen_urls
from scraper.messaging.producer import send_batch_event

SEEN_FILE = "scraper/state/le360/seen_urls_batch.json"

def run_le360_batch():
    """Lance un cycle de scraping batch Le360 (une seule fois)."""
    seen_urls = set(load_seen_urls(SEEN_FILE))
    links = get_article_links()
    new_articles = []

    for link in links:
        url = link["url"]
        if url not in seen_urls:
            print(f"\nNouvel article détecté : {url}")
            article_data = scrape_article(url)
            article_data["category"] = link["category"]
            article_data["title"] = link["title"]
            new_articles.append(article_data)

    if new_articles:
        for article in new_articles:
            send_batch_event(article)
            seen_urls.add(article["url"])
        save_seen_urls(list(seen_urls), SEEN_FILE)
        print(f"[LE360 BATCH] ✓ {len(new_articles)} nouveaux articles envoyés")
    else:
        print("[LE360 BATCH] Aucun nouvel article")