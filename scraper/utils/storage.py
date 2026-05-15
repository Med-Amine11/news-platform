# Contient les URLs déjà traitées 

import json 
import os
from datetime import datetime


def load_seen_urls(SEEN_FILE) : 
    # Si le fichier n'existe pas 
    if not os.path.exists(SEEN_FILE) :
        return []
    
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []
    
def save_seen_urls(urls , SEEN_FILE):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(
            urls,
            f,
            ensure_ascii=False, # on veut écrire les vrais caractères au lieu des références Unicode
            indent=4 # rend le JSON lisible 
        )

def save_article(ARTICLES_DATA_PATH, article):

    os.makedirs(
        "data",
        exist_ok=True
    )

    article["ingestion_time"] = (
        datetime.utcnow().isoformat()
    )

    with open(
        ARTICLES_DATA_PATH , 
        "a",
        encoding="utf-8"
    ) as f:

        json.dump(
            article,
            f,
            ensure_ascii=False
        )

        f.write("\n")
