
import json
import threading
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
# Pour écouter les messages envoyés par les scrapers
from kafka import KafkaConsumer
from scraper.warehouse.schema import  create_tables

from scraper.modes.hespress.batch import run_hespress_batch
from scraper.modes.hespress.stream import run_hespress_stream
from scraper.modes.le360.batch import run_le360_batch
from scraper.modes.le360.stream import run_le360_stream

from scraper.lake.bronze.stream import save_bronze
from scraper.lake.silver.stream import save_silver
from scraper.lake.gold.stream import save_gold
from scraper.lake.bronze.batch import save_bronze_batch
from scraper.lake.silver.batch import save_silver_batch
from scraper.lake.gold.batch import save_gold_batch

# Configure les logs avec hordotage
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

log = logging.getLogger(__name__)


# ─── CONSUMERS ────────────────────────────────────────────

def run_stream_consumer():
    log.info("[STREAM CONSUMER] ▶ En attente de messages...")
    consumer = KafkaConsumer(
        "articles_stream",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        consumer_timeout_ms=120000 # s'arrête après 2min sans message
    )
    keys = []
    for message in consumer:
        try:
            article = message.value
            save_bronze(article)
            article_silver = save_silver(article)
            key = save_gold(article_silver)
            keys.append(key)
        except Exception as e:
            log.error(f"[STREAM CONSUMER] Erreur : {e}")
    log.info(f"[STREAM CONSUMER] ✓ {len(keys)} articles traités")


def run_batch_consumer():
    log.info("[BATCH CONSUMER] ▶ En attente de messages...")
    consumer = KafkaConsumer(
        "articles_batch",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        consumer_timeout_ms=120000
    )
    articles = []
    for message in consumer:
        try:
            article = message.value
            articles.append(article)
            log.info(f"[BATCH CONSUMER] Article reçu : {article['title']}")
        except Exception as e:
            log.error(f"[BATCH CONSUMER] Erreur : {e}")

    if articles:
        save_bronze_batch(articles)
        articles_silver = save_silver_batch(articles)
        save_gold_batch(articles_silver)
        log.info(f"[BATCH CONSUMER] ✓ {len(articles)} articles traités")
    else:
        log.info("[BATCH CONSUMER] Aucun article reçu")


# ─── JOBS ─────────────────────────────────────────────────

def job_stream():
    log.info("[SCHEDULER] ══════ Job STREAM démarré ══════")

    # Étape 1 — Consumer démarre en premier (écoute Kafka)
    consumer_thread = threading.Thread(
        target=run_stream_consumer,
        name="stream-consumer"
    )
    consumer_thread.start()

    # Étape 2 — Scrapers démarrent après (produisent dans Kafka)
    hespress_thread = threading.Thread(
        target=run_hespress_stream,
        name="hespress-stream"
    )
    le360_thread = threading.Thread(
        target=run_le360_stream,
        name="le360-stream"
    )

    hespress_thread.start()
    le360_thread.start()

    # Attendre que tout soit terminé
    hespress_thread.join()
    le360_thread.join()
    consumer_thread.join()

    log.info("[SCHEDULER] ══════ Job STREAM terminé ══════\n")


def job_batch():
    log.info("[SCHEDULER] ══════ Job BATCH démarré ══════")

    # Étape 1 — Consumer démarre en premier (écoute Kafka)
    consumer_thread = threading.Thread(
        target=run_batch_consumer,
        name="batch-consumer"
    )
    consumer_thread.start()

    # Étape 2 — Scrapers démarrent après (produisent dans Kafka)
    hespress_thread = threading.Thread(
        target=run_hespress_batch,
        name="hespress-batch"
    )
    le360_thread = threading.Thread(
        target=run_le360_batch,
        name="le360-batch"
    )

    hespress_thread.start()
    le360_thread.start()

    # Attendre que tout soit terminé
    hespress_thread.join()
    le360_thread.join()
    consumer_thread.join()

    log.info("[SCHEDULER] ══════ Job BATCH terminé ══════\n")


# ─── MAIN ─────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("[SCHEDULER] Initialisation...")

    # Créer les tables PostgreSQL au démarrage
    create_tables()
    
    # Bloque le programme principal et tourne indéfiniment jusqu'à Ctrl + C
    scheduler = BlockingScheduler()

    # IntervalTrigger définit l'intervalle de répétition
    scheduler.add_job(
        job_stream,
        trigger=IntervalTrigger(minutes=2),
        id="stream_job",
        name="Stream Hespress + Le360",
        replace_existing=True
    )

    # Batch toutes les heures
    scheduler.add_job(
        job_batch,
        trigger=IntervalTrigger(minutes = 5),
        id="batch_job",
        name="Batch Hespress + Le360",
        replace_existing=True
    )

    log.info("═══════════════════════════════════════")
    log.info("  Scheduler démarré")
    log.info("  Stream  : toutes les 5 minutes")
    log.info("  Batch   : toutes les heures")
    log.info("  Ctrl+C  : arrêter proprement")
    log.info("═══════════════════════════════════════\n")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        log.info("[SCHEDULER] Arrêt propre...")
        scheduler.shutdown()