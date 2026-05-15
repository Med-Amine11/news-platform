from scraper.warehouse.connection import get_connection

def create_tables():
    
    # Créer une connexion vers la base
    conn = get_connection()
    
    # Créer un objet de type Cursor permet de  : 
        # Exécuter des requetes SQL
        # envoyer des commandes à la base
        # Récupérer des résultats
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS by_source (
            id SERIAL PRIMARY KEY,
            source VARCHAR(100),
            article_count INTEGER,
            generated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS by_day (
            id SERIAL PRIMARY KEY,
            day DATE,
            article_count INTEGER,
            generated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS by_category (
            id SERIAL PRIMARY KEY,
            category VARCHAR(100),
            article_count INTEGER,
            generated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS by_lang (
            id SERIAL PRIMARY KEY,
            lang VARCHAR(50),
            article_count INTEGER,
            generated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS top_tags (
            id SERIAL PRIMARY KEY,
            keyword VARCHAR(100),
            count INTEGER,
            generated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS top_keywords_titles (
            id SERIAL PRIMARY KEY,
            keyword VARCHAR(100),
            count INTEGER,
            generated_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS top_keywords_content (
            id SERIAL PRIMARY KEY,
            keyword VARCHAR(100),
            count INTEGER,
            generated_at TIMESTAMP
        );
    """)
    
    # Valider définitivement les changements dans la base 
    conn.commit()
    cur.close()
    conn.close()
    print("[WAREHOUSE] ✓ Tables créées")
    
def drop_tables():
    
    # Connexion à la base
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS top_keywords_content;
        DROP TABLE IF EXISTS top_keywords_titles;
        DROP TABLE IF EXISTS top_tags;
        DROP TABLE IF EXISTS by_lang;
        DROP TABLE IF EXISTS by_category;
        DROP TABLE IF EXISTS by_day;
        DROP TABLE IF EXISTS by_source;
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("[WAREHOUSE] ✓ Tables supprimées")
