from datetime import datetime
from scraper.utils.key import make_key
from scraper.lake.gold.transform import to_gold , build_analytics
from scraper.utils.minio_client import save_object
from scraper.warehouse.insert import insert_analytics

def save_analytics(table_name, data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    key = f"analytics/{table_name}/{timestamp}.json"
    save_object("gold", key, data)
    print(f"[GOLD BATCH] ✓ {key}")
    
    # PostgreSQL 
    insert_analytics(table_name, data)
    
    
    
def save_gold_batch(articles_silver):
    """
    1 — Enrichit et sauvegarde chaque article dans gold/
    2 — Génère et sauvegarde les tables analytiques dans gold/analytics/
    """
    keys = []

    # Enrichissement article par article
    for article_silver in articles_silver :
        article_gold   = to_gold(article_silver)
        key = make_key(article_gold, mode="batch")
        save_object("gold", key, article_gold)
        keys.append(key)
    
    print(f"[GOLD BATCH] ✓ {len(keys)} articles enrichis")
    
    analytics = build_analytics(articles_silver)
    
    for table_name in ["by_source", "by_day", "by_category", "by_lang",
                       "top_tags", "top_keywords_titles", "top_keywords_content"]:
        save_analytics(table_name, {
            "data":         analytics[table_name],
            "generated_at": analytics["generated_at"]
        })

    return keys