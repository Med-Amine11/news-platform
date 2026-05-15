import re
from stopwordsiso import stopwords
from datetime import datetime
from collections import Counter

STOPWORDS_FR = stopwords("fr")
STOPWORDS_EN = stopwords("en")
STOPWORDS_AR = stopwords("ar")

# Stream : enrichissement article par article 
def to_gold(article_silver):
    """
    Enrichit un article silver avec des métriques calculées
    """
    content = article_silver.get("content", "")
    title   = article_silver.get("title", "")

    return {
        **article_silver, # Décomposer le dict article_silver
        "word_count":    len(content.split()),
        "title_length":  len(title),
        "has_author":    bool(article_silver.get("author")),
        "has_tags":      len(article_silver.get("tags", [])) > 0,
        "has_content":   len(content) > 0,
        "enriched_at":   datetime.now().isoformat(),
    }

def extract_keywords(text, top_n=20):
    
    # Extraire les mots français/anglais et arabes en même temps
    words_latin  = re.findall(r'\b[a-zA-ZÀ-ÿ]{4,}\b', text.lower())
    words_arabic = re.findall(r'[\u0600-\u06FF]{3,}', text)

    # Combiner les deux listes
    all_words = words_latin + words_arabic

    # Filtrer les stopwords des 3 langues
    all_words = [
        w for w in all_words
        if w not in STOPWORDS_FR
        and w not in STOPWORDS_AR
        and w not in STOPWORDS_EN
    ]

    return Counter(all_words).most_common(top_n) # Trier par ordre de fréquence

def build_analytics(articles):
    """
    Génère toutes les tables analytiques à partir des articles silver
    """

    # ── Articles par source ──
    by_source = Counter(a.get("source") for a in articles).most_common()
    
    # ── Articles par jour ──
    by_day = Counter(
    # Utilise date si elle existe, sinon ingestion_time
    (a.get("date") or a.get("ingestion_time", ""))[:10]  # "2026-05-14 06:00" → "2026-05-14"
    for a in articles
    if a.get("date") or a.get("ingestion_time")
     )

    # ── Articles par catégorie ──
    by_category = Counter(a.get("category") for a in articles).most_common()

    # ── Articles par langue ──
    by_lang = Counter(a.get("lang") for a in articles).most_common()

    # ── Top tags ──
    all_tags = [tag for a in articles for tag in a.get("tags", [])]
    top_tags = Counter(all_tags).most_common(20) # Trier par ordre de fréquence

    # ── Top mots clés (titres) ──
    all_titles = " ".join(a.get("title", "") for a in articles)
    top_keywords_titles = extract_keywords(all_titles, top_n=20)

    # ── Top mots clés (contenu) ──
    all_content = " ".join(a.get("content", "") for a in articles)
    top_keywords_content = extract_keywords(all_content, top_n=30)
    
    return {
    "by_source":            dict(by_source),
    "by_day":               dict(sorted(by_day.items())),  # .items() → liste de tuples (clé, valeur)
     # exemple :Counter({"2026-05-14": 38,"2026-05-12": 45,"2026-05-13": 62})  → [("2026-05-14", 38), ("2026-05-12", 45), ("2026-05-13", 62)]
    "by_category":          dict(by_category),
    "by_lang":              dict(by_lang),
    "top_tags":             dict(top_tags),
    "top_keywords_titles":  dict(top_keywords_titles),
    "top_keywords_content": dict(top_keywords_content),
    "total_articles":       len(articles),
    "generated_at":         datetime.now().isoformat(),
}