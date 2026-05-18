import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.deps import get_ingestion_service
from app.core.config import get_settings
from app.core.security import verify_api_key
from app.models.upload_models import UploadResponse
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/upload", tags=["upload"], dependencies=[Depends(verify_api_key)])
logger = logging.getLogger(__name__)


@router.post("", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
) -> UploadResponse:
    logger.info("Upload action started for file: %s", file.filename)
    settings = get_settings()
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )
    raw = await file.read()
    logger.info("File read into memory for file=%s, size=%.2fMB", file.filename, len(raw) / (1024 * 1024))
    if len(raw) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File is too large",
        )
    try:
        doc_id, chunk_count = await ingestion_service.ingest_file_async(file.filename, raw)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Upload action failed for file=%s: %s", file.filename, exc)
        detail = "Upload failed during processing. Check backend logs for provider/storage details."
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        exc_text = str(exc).lower()
        if any(token in exc_text for token in ["failed to connect", "permission denied", "timed out", "timeout"]):
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            detail = "Upload failed because model/storage provider is unreachable from backend network."
        raise HTTPException(
            status_code=status_code,
            detail=detail,
        ) from exc
    logger.info("Upload action completed for document_id=%s, chunks=%s", doc_id, chunk_count)
    return UploadResponse(
        document_id=doc_id,
        filename=file.filename,
        chunks_created=chunk_count,
        status="processed",
        message="Document uploaded and indexed successfully",
    )
