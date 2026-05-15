from scraper.utils.minio_client import save_object
from scraper.utils.key import make_key

def save_bronze_batch(articles):
    keys = []

    for article in articles:
        key = make_key(article, mode="batch")
        save_object("bronze", key, article)
        keys.append(key)

    print(f"[BRONZE BATCH] ✓ {len(keys)} articles sauvegardés")
    return keys