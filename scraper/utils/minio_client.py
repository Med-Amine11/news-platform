import json
from io import BytesIO
from minio import Minio

# Objet Python pour connecter avec le serveur MinIO
client = Minio(
    "localhost:9000",   # adresse du serveur MinIO
    access_key="admin",
    secret_key="password123",
    secure=False   # pas de HTTPS (on est en local)
)

BUCKETS = ["bronze", "silver", "gold"]

for bucket in BUCKETS:
    if not client.bucket_exists(bucket):  # envoie une vraie requête au serveur
        client.make_bucket(bucket)   # crée le bucket s'il n'existe pas
        print(f"Bucket '{bucket}' créé")
    else:
        print(f"Bucket '{bucket}' existe déjà")

def save_object(bucket, key, data):
    payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    client.put_object(
        bucket, key,
        BytesIO(payload),
        length=len(payload),
        content_type="application/json"
    )