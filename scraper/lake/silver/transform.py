import re
from datetime import datetime
from langdetect import detect

def normalize_text(text):
    """Nettoie un texte : espaces multiples, caractères invisibles"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u200b', '') # Zero with space : carctère invisible 
    text = text.replace('\xa0', ' ') # Non-Breaking Space : empeche le retour à la ligne 
    return text.strip()


def _translate_month(date_str):
    """Traduit les mois français en anglais pour le parsing"""
    months = {
        "janvier": "January", "février": "February", "mars": "March",
        "avril": "April",     "mai": "May",           "juin": "June",
        "juillet": "July",    "août": "August",       "septembre": "September",
        "octobre": "October", "novembre": "November", "décembre": "December"
    }
    for fr, en in months.items():
        date_str = date_str.replace(fr, en)
    return date_str


def normalize_content(content):
    """
    Unifie le contenu en un seul texte propre
    - Hespress : string avec \\n → on split et on joint
    - Le360    : liste de paragraphes → on joint
    """
    if isinstance(content, list):
        # Le360 : liste de paragraphes
        return " ".join([
            normalize_text(p)
            for p in content
            if p.strip()
        ])
    elif isinstance(content, str):
        # Hespress : string avec \n
        paragraphs = content.split('\n')
        return " ".join([
            normalize_text(p)
            for p in paragraphs
            if p.strip()
        ])
    return ""

def normalize_date(date_str, source):
    """
    Normalise la date selon la source
    - Hespress : "mercredi 13 mai 2026 - 18:16" → "2026-05-13 18:16"
    - Le360    : "Le 14/05/2026 à 06h00"         → "2026-05-14 06:00"
    """
    if not date_str:
        return ""

    try:
        if source == "Hespress":
            # Supprimer le jour de la semaine : "mercredi 13 mai 2026 - 18:16"
            date_str = re.sub(r'^(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)\s+', '', date_str, flags=re.IGNORECASE)
            # Traduire les mois français
            date_str = _translate_month(date_str)
            dt = datetime.strptime(date_str, "%d %B %Y - %H:%M")
            return dt.strftime("%Y-%m-%d %H:%M")

        elif source == "Le360":
            date_str = date_str.replace("Le ", "").strip()
            dt = datetime.strptime(date_str, "%d/%m/%Y à %Hh%M")
            return dt.strftime("%Y-%m-%d %H:%M")

    except Exception:
        return date_str

    return date_str

def detect_lang(text):
    """Détecte la langue du contenu"""
    try:
        return detect(text) if text else "unknown"
    except Exception:
        return "unknown"

def to_silver(article):
    """
    Transforme un article brut (bronze) en article nettoyé (silver)
    Gère les deux formats Hespress et Le360
    """
    source  = article.get("source")
    content = normalize_content(article.get("content", ""))
    return {
        "url":            article["url"],
        "source":         source,
        "title":          normalize_text(article.get("title")),
        "author":         normalize_text(article.get("author") ),
        "date":           normalize_date(article.get("date"), source),
        "category":       normalize_text(article.get("category")),
        "tags":           [t.strip() for t in article.get("tags") if t.strip()],
        "content":        content,
        "lang":           detect_lang(content) if content else "visual_content",
        "processed_at":   datetime.now().isoformat(),
    }