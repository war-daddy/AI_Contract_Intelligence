# app/services/rag.py

from app.services.embedding import generate_embedding
from app.services.retriever import semantic_search
from app.services.llm import call_llm

def rag_pipeline(query: str, db):
    """
    Full RAG pipeline:
    1. Embed query
    2. Retrieve relevant chunks
    3. Pass to LLM
    """

    query_vector = generate_embedding(query)

    results = semantic_search(db, query_vector)

    context = "\n".join([str(r) for r in results])

    prompt = f"""
    You are a legal AI assistant.
    
    Context:
    {context}

    Question:
    {query}

    Output JSON:
    {{
        "risk_level": "",
        "issues": [],
        "recommendation": ""
    }}
    """

    return call_llm(prompt)