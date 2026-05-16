from scraper.core.le360.links import get_article_links
from scraper.core.le360.article import scrape_article
from scraper.utils.storage import load_seen_urls, save_seen_urls, save_article
from scraper.messaging.producer import send_stream_event

SEEN_FILE = "scraper/state/le360/seen_urls_stream.json"

def run_le360_stream():
    """Lance un cycle de scraping stream Le360 (une seule fois)."""
    seen_urls = set(load_seen_urls(SEEN_FILE))
    links = get_article_links(nb_clicks=1)
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
            send_stream_event(article)
            seen_urls.add(article["url"])
        save_seen_urls(list(seen_urls), SEEN_FILE)
        print(f"[LE360 STREAM] ✓ {len(new_articles)} nouveaux articles envoyés")
    else:
        print("[LE360 STREAM] Aucun nouvel article")