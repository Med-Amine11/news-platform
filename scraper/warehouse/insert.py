from scraper.warehouse.connection import get_connection
from datetime import datetime

def insert_analytics(table_name, data):
    conn = get_connection()
    cur = conn.cursor()
    generated_at = data.get("generated_at", datetime.now().isoformat())
    rows = data.get("data", {})

    if table_name == "by_source":
        for source, count in rows.items():
            cur.execute(
                "INSERT INTO by_source (source, article_count, generated_at) VALUES (%s, %s, %s)",
                (source, count, generated_at)
            )

    elif table_name == "by_day":
        for day, count in rows.items():
            cur.execute(
                "INSERT INTO by_day (day, article_count, generated_at) VALUES (%s, %s, %s)",
                (day, count, generated_at)
            )

    elif table_name == "by_category":
        for category, count in rows.items():
            cur.execute(
                "INSERT INTO by_category (category, article_count, generated_at) VALUES (%s, %s, %s)",
                (category, count, generated_at)
            )

    elif table_name == "by_lang":
        for lang, count in rows.items():
            cur.execute(
                "INSERT INTO by_lang (lang, article_count, generated_at) VALUES (%s, %s, %s)",
                (lang, count, generated_at)
            )

    elif table_name in ("top_tags", "top_keywords_titles", "top_keywords_content"):
     for keyword, count in rows.items():  
        cur.execute(
            f"INSERT INTO {table_name} (keyword, count, generated_at) VALUES (%s, %s, %s)",
            (keyword, count, generated_at)
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f"[WAREHOUSE] ✓ {table_name} inséré")