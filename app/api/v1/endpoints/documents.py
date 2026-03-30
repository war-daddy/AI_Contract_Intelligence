# app/api/v1/endpoints/documents.py

from fastapi import APIRouter, UploadFile
from app.workers.tasks import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile):
    """
    Upload → send to async worker
    """
    file_path = f"/tmp/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    process_document.delay(file_path)

    return {"message": "Processing started"}