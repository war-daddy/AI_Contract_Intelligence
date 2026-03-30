# app/api/v1/endpoints/query.py

from fastapi import APIRouter, Depends
from app.services.rag import rag_pipeline
from app.db.session import get_db

router = APIRouter()

@router.post("/ask")
def ask_question(query: str, db=Depends(get_db)):
    """
    Query contract using RAG pipeline.
    """
    return rag_pipeline(query, db)