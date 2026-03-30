# app/services/retriever.py

from sqlalchemy.orm import Session
from app.db.models.embedding import Embedding
from sqlalchemy import text

def semantic_search(db: Session, query_vector, limit=5):
    """
    Uses pgvector cosine similarity.
    """
    sql = text("""
        SELECT * FROM embeddings
        ORDER BY vector <-> :query_vector
        LIMIT :limit
    """)

    return db.execute(sql, {
        "query_vector": query_vector,
        "limit": limit
    }).fetchall()