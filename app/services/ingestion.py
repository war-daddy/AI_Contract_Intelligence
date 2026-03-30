# app/services/ingestion.py

from pymupdf import open as fitz_open

def extract_text(file_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF.
    """
    doc = fitz_open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def chunk_text(text: str, chunk_size=500, overlap=50):
    """
    Splits text into overlapping chunks.
    WHY: improves retrieval accuracy in RAG.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks