# app/services/llm.py

import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def call_llm(prompt: str):
    """
    Central LLM wrapper.
    WHY: easy to swap providers later.
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a legal expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content