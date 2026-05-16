# 📰 News Platform — Pipeline de données en temps réel

Plateforme automatisée de collecte, traitement et analyse des articles de presse marocaine depuis **Hespress** et **Le360**.

---

## 🏗️ Architecture globale

```
┌─────────────┐     ┌─────────────┐
│   Hespress  │     │    Le360    │
└──────┬──────┘     └──────┬──────┘
       │                   │
       ▼                   ▼
┌─────────────────────────────────┐
│         Apache Kafka            │
│   topic: articles_stream        │
│   topic: articles_batch         │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│          Data Lake MinIO        │
│   Bronze │ Silver │ Gold        │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│         PostgreSQL              │
│   Data Warehouse (Analytics)    │
└─────────────────┬───────────────┘
                  │
                  ▼
┌─────────────────────────────────┐
│           Grafana               │
│   Dashboard & Visualisation     │
└─────────────────────────────────┘
```

---

## 🛠️ Technologies utilisées

| Outil | Rôle |
|-------|------|
| **Python** | Langage principal (scraping, traitement, orchestration) |
| **Apache Kafka** | Message broker entre scrapers et consumers |
| **Zookeeper** | Gestion du cluster Kafka |
| **MinIO** | Data Lake — stockage objet compatible S3 |
| **PostgreSQL** | Data Warehouse — analytics agrégées |
| **Grafana** | Dashboard de visualisation |
| **APScheduler** | Orchestration et automatisation des jobs |
| **Docker** | Conteneurisation de tous les services |

---

## 📁 Structure du projet

```
news-platform/
├── docker-compose.yml            ← Infrastructure complète (Zookeeper,Kafka, MinIO, PostgreSQL, Grafana)
├── README.md
└── scraper/
    │
    ├── scheduler.py              ← Point d'entrée principal — orchestre tous les jobs
    │
    ├── core/                     ← Scraping bas niveau (récupération des liens et du contenu)
    │   ├── hespress/
    │   │   ├── links.py          ← Récupère tous les liens d'articles (mode batch)
    │   │   ├── stream_links.py   ← Récupère les derniers liens uniquement (mode stream)
    │   │   └── article.py        ← Scrape le contenu complet d'un article Hespress
    │   └── le360/
    │   |   ├── links.py          ← Récupère les liens + catégorie + titre (batch et stream)
    │   |   |__ article.py        ← Scrape le contenu complet d'un article Le360
    |   |        
    │    ── driver.py         ← Gestion du navigateur Selenium pour Hespress (infinite scroll)
    │
    ├── modes/                    ← Orchestration du scraping par source et par mode
    │   ├── hespress/
    │   │   ├── batch.py          ← run_hespress_batch() — un cycle complet Hespress batch
    │   │   └── stream.py         ← run_hespress_stream() — un cycle complet Hespress stream
    │   └── le360/
    │       ├── batch.py          ← run_le360_batch() — un cycle complet Le360 batch
    │       └── stream.py         ← run_le360_stream() — un cycle complet Le360 stream
    │
    ├── lake/                     ← Data Lake — Architecture Médaillon (Bronze / Silver / Gold)
    │   ├── bronze/
    │   │   ├── stream.py         ← save_bronze() — sauvegarde un article brut dans MinIO
    │   │   └── batch.py          ← save_bronze_batch() — sauvegarde un lot d'articles bruts
    │   ├── silver/
    │   │   ├── stream.py         ← save_silver() — nettoie et sauvegarde un article
    │   │   ├── batch.py          ← save_silver_batch() — nettoie et sauvegarde un lot
    │   │   └── transform.py      ← Fonctions de nettoyage (suppression HTML, normalisation, détection langue)
    │   └── gold/
    │       ├── stream.py         ← save_gold() — enrichit et sauvegarde un article
    │       ├── batch.py          ← save_gold_batch() — enrichit + génère les analytics
    │       └── transform.py      ← Fonctions d'enrichissement (métriques, analytics agrégées)
    │
    ├── warehouse/                ← Data Warehouse PostgreSQL
    │   ├── connection.py         ← Connexion à PostgreSQL (host, port, user, password)
    │   ├── schema.py             ← Création des 7 tables analytiques au démarrage
    │   └── insert.py             ← Insertion des analytics dans PostgreSQL
    │
    ├── messaging/                ← Communication avec Kafka
    │   └── producer.py           ← send_stream_event() et send_batch_event()
    │
    ├── utils/                    ← Utilitaires partagés
    │   ├── storage.py            ← load_seen_urls(), save_seen_urls(), save_article() 
    |   |                                            
    │   ├── minio_client.py       ← Initialisation et connexion au client MinIO
    │   └── key.py                ← Génération des clés de stockage MinIO (chemins des fichiers)
    │
    |__state/
        ├── hespress/
        │   ├── seen_urls_stream.json   ← utilisé uniquement par le stream
        │   └── seen_urls_batch.json    ← utilisé uniquement par le batch
        └── le360/
            ├── seen_urls_stream.json
            └── seen_urls_batch.json


---

## 🚀 Installation & Démarrage

### Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Python 3.10+

### 1 — Cloner le projet

```bash
git clone https://github.com/Med-Amine11/news-platform
cd news-platform
```

### 2 — Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 3 — Démarrer les services Docker

```bash
docker-compose up -d
```

Les services suivants démarrent automatiquement :

| Service | URL |
|---------|-----|
| MinIO Console | http://localhost:9001 |
| Grafana | http://localhost:3000 |
| Kafka | localhost:9092 |
| PostgreSQL | localhost:5432 |

### 4 — Lancer le pipeline

```bash
cd news-platform
python -m scraper.scheduler
```

---

## ⚙️ Configuration

### Docker — Identifiants

| Service | Utilisateur | Mot de passe |
|---------|-------------|--------------|
| MinIO | `admin` | `password123` |
| PostgreSQL | `admin` | `admin123` |
| Grafana | `admin` | `admin123` |

### Intervalles du scheduler

| Job | Intervalle (test) | Intervalle (production) |
|-----|-------------------|--------------------------|
| Stream (Hespress + Le360) | Toutes les 2 minutes | Toutes les 2 minutes |
| Batch (Hespress + Le360) | Toutes les 5 minutes | Toutes les 5 heures |

---

## 🗄️ Data Lake — Architecture Médaillon

### Bronze — Données brutes
Sauvegarde exacte de l'article tel que scraipé, sans aucune modification.

```json
{
  "url": "https://hespress.com/...",
  "title": "Titre original",
  "content": "Contenu brut avec HTML..." , 
  "source" : "Source" , 
  "author": "Auteur", 
  "date" : "Date de publication" ,
  "tags" : ["tag 1" , "tag 2" , ... ]
  "category" : "Catégorie"
}
```

### Silver — Données nettoyées
HTML supprimé, champs normalisés, langue détectée.

```json

{
  "url": "https://hespress.com/...",
  "title": "Titre nettoyé",
  "content": "Contenu propre...",
  "author": "Nom auteur",
  "tags": ["Politique", "Maroc"],
  "lang": "ar" , 
  "processed_at": "..." , 
  ...
}
```

### Gold — Données enrichies + Analytics
Métriques calculées sur chaque article + tables analytiques agrégées.

```json
{
  "word_count": 320,
  "title_length": 65,
  "has_author": true,
  "has_tags": true,
  "has_content": true
}
```

---

## 📊 Data Warehouse — Tables PostgreSQL

| Table | Description |
|-------|-------------|
| `by_source` | Nombre d'articles par source (Hespress / Le360) |
| `by_day` | Nombre d'articles publiés par jour |
| `by_category` | Nombre d'articles par catégorie |
| `by_lang` | Nombre d'articles par langue (ar / fr / unknown) |
| `top_tags` | Tags les plus utilisés |
| `top_keywords_titles` | Mots-clés les plus fréquents dans les titres |
| `top_keywords_content` | Mots-clés les plus fréquents dans le contenu |

---

## 📈 Dashboard Grafana

Dashboard créé via l'interface web Grafana — 6 panels connectés à PostgreSQL, chacun lié à une requête SQL dédiée.

**Panels disponibles :**
- Articles par source (Bar chart)
- Articles par jour (Time series)
- Articles par langue (Pie chart)
- Top tags (Bar chart)
- Top mots-clés titres (Bar chart)
- Top mots-clés contenu (Bar chart)

---

## 🔄 Orchestration — APScheduler

```
Démarrage
├── job_stream → lance immédiatement, puis toutes les 2 min
│     ├── Thread 1 : Consumer stream écoute Kafka
│     ├── Thread 2 : Hespress scrape + envoie Kafka
│     └── Thread 3 : Le360 scrape + envoie Kafka
│
└── job_batch → lance immédiatement, puis toutes les 5 min
      ├── Thread 1 : Consumer batch écoute Kafka
      ├── Thread 2 : Hespress scrape + envoie Kafka
      └── Thread 3 : Le360 scrape + envoie Kafka
                     └── Gold Batch → PostgreSQL → Grafana
```

---

## 🐳 Services Docker

```yaml
Services     Port
zookeeper  → 2181
kafka      → 9092
minio      → 9000 (API) / 9001 (Console)
postgres   → 5432
grafana    → 3000
```

**Commandes utiles :**

```bash
# Démarrer tous les services
docker-compose up -d

# Arrêter tous les services
docker-compose down

# Voir les logs d'un service
docker logs -f postgres

# Accéder à PostgreSQL
docker exec -it postgres psql -U admin -d news_warehouse
```

---

## 📦 Dépendances Python

```
kafka-python
minio
psycopg2-binary
apscheduler
beautifulsoup4
requests
langdetect
```

---

## 👥 Auteurs

- Mehdi Ammal
- Mohamed Amine Aswab

---

## 📄 Licence

Ce projet est développé dans le cadre d'un projet académique.
