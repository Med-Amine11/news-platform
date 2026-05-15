from scraper.utils.minio_client import save_object
from scraper.utils.key import make_key
from scraper.lake.silver.transform import to_silver


def save_silver_batch(articles):
    
    keys =[]
    articles_silver = []
    
    for article in articles:
        article_silver = to_silver(article)
        key = make_key(article, mode="batch")
        save_object("silver", key, article_silver)
        articles_silver.append(article_silver)
        keys.append(key)

    print(f"[SILVER BATCH] ✓ {len(keys)} articles traités")
    return articles_silver