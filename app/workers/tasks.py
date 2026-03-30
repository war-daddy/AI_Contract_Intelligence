# app/workers/tasks.py

from celery import Celery
from app.services.ingestion import extract_text, chunk_text
from app.services.embedding import generate_embedding

celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task
def process_document(file_path: str):
    """
    Async pipeline:
    - extract text
    - chunk
    - generate embeddings
    """

    text = extract_text(file_path)
    chunks = chunk_text(text)

    for chunk in chunks:
        emb = generate_embedding(chunk)
        # store in DB (pseudo)
        print("Stored embedding:", emb[:5])