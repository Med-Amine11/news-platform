from scraper.utils.minio_client import client, save_object
from scraper.utils.key import make_key


def save_bronze(article):
    key = make_key(article, mode="stream")
    save_object("bronze", key, article)
    print(f"[BRONZE] ✓ {key}")
    return key