import hashlib
import re

def slugify(title):
    """
    Transforme un titre en slug lisible pour le nom du fichier
    Exemple : "Le gouvernement annonce une réforme" → "le-gouvernement-annonce-une-reforme"
    """
    # Mettre en minuscules
    title = title.lower().strip()
    
    # Remplacer les espaces par des tirets
    title = re.sub(r'\s+', '-', title)
    
    # Supprimer les caractères spéciaux (garder lettres, chiffres, tirets)
    title = re.sub(r'[^\w\-]', '', title)
    
    # Remplacer les tirets multiples par un seul
    title = re.sub(r'-+', '-', title)
    
    # Limiter la longueur pour éviter des noms de fichiers trop longs
    return title[:80]


def make_key(article, mode):
    """
    Génère une clé unique pour identifier un article dans MinIO
    
    La clé suit ce format :
    {source}/{mode}/{url_hash}_{slug}.json
    
    Exemple :
    hespress/stream/a3f9b2c1_le-gouvernement-annonce-une-reforme.json
    
    Paramètres :
    - article : dictionnaire contenant les données de l'article
    - mode    : "stream" ou "batch" selon le type de traitement
    """

    # Récupérer la source de l'article (hespress, le360...)
    source = article["source"]

    # Générer un hash court de l'URL (8 caractères)
    # MD5 de l'URL garantit que le même article aura toujours la même clé
    # ce qui évite les doublons si l'article est traité deux fois
    url_hash = hashlib.md5(article["url"].encode()).hexdigest()[:8]

    # Générer le slug à partir du titre
    slug = slugify(article["title"])

    # Construire la clé finale
    key = f"{source}/{mode}/{url_hash}_{slug}.json"

    return key