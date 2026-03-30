# app/services/embedding.py

import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_embedding(text: str):
    """
    Calls embedding model.
    NOTE: In production, batch this to reduce cost.
    """
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding