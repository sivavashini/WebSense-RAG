import re
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from services.config import settings
from services.database import add_document
from services.document_loader import extract_text, validate_upload
from services.vector_store import index_text
from services.websocket import manager

router = APIRouter(tags=["upload"])


def safe_name(filename: str) -> str:
    name = Path(filename).name
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    try:
        validate_upload(file.filename or "document", len(data), settings.max_upload_mb)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    filename = safe_name(file.filename or "document")
    path = settings.upload_path / filename
    path.write_bytes(data)
    await manager.broadcast({"type": "upload_saved", "filename": filename})

    try:
        text = extract_text(path)
        if not text.strip():
            raise ValueError("No readable text found in the uploaded file.")
        chunks = index_text(filename, text)
        add_document(filename, chunks)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not index file: {exc}") from exc

    await manager.broadcast({"type": "upload_indexed", "filename": filename, "chunks": chunks})
    return {"filename": filename, "chunks": chunks, "status": "indexed", "vector_store": "FAISS"}
