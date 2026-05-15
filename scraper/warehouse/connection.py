# Driver PostgreSQL
# Permet à Pyhton de communiquer avec la base de données PostgreSQL
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="news_warehouse",
        user="admin",
        password="admin123"
    )

