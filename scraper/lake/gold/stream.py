from scraper.utils.minio_client import save_object
from scraper.utils.key import make_key
from scraper.lake.gold.transform import to_gold


def save_gold(article_silver):
    """
    Silver → Gold pour un seul article
    """
    article_gold   = to_gold(article_silver)

    key = make_key(article_gold, mode="stream")
    save_object("gold", key, article_gold)
    print(f"[GOLD STREAM] ✓ {key}")
    return key