# Transformer les objets Python en texte JSON
import json 

# Importer le client Python pour envoyer des messages à kafka
from kafka import KafkaProducer

# Création du producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092", # Adresse du serveur kafka 
    value_serializer=lambda v: # Transformer l'objet Python en message kafka
    json.dumps(v, ensure_ascii=False)
    .encode("utf-8")
)


TOPIC_STREAM = "articles_stream"
def send_stream_event(article):
    producer.send(TOPIC_STREAM, value=article)
    producer.flush()

TOPIC_BATCH  = "articles_batch"
def send_batch_event(article):
    producer.send(TOPIC_BATCH, value=article)
    producer.flush()
