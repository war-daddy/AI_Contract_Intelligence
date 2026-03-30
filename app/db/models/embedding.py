# app/db/models/embedding.py

from sqlalchemy import Column, Integer, ForeignKey
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    # Vector embedding stored in pgvector
    vector = Column(Vector(1536))