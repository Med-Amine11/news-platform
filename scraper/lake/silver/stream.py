from scraper.utils.minio_client import save_object
from scraper.utils.key import make_key
from scraper.lake.silver.transform import to_silver


def save_silver(article):
    article_silver = to_silver(article)
    key = make_key(article, mode="stream")
    save_object("silver", key, article_silver)
    print(f"[SILVER STREAM] ✓ {key}")
    return article_silver