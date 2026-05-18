import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_document_service
from app.core.security import verify_api_key
from app.models.document_models import DocumentDeleteResponse, DocumentInfo, DocumentListResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"], dependencies=[Depends(verify_api_key)])
logger = logging.getLogger(__name__)


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentListResponse:
    logger.info("List documents action started")
    items = [DocumentInfo(**d) for d in await document_service.list_documents_async()]
    logger.info("List documents action completed, count=%s", len(items))
    return DocumentListResponse(items=items)


@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
async def delete_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentDeleteResponse:
    logger.info("Delete document action started for document_id=%s", document_id)
    deleted = await document_service.delete_document_async(document_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    logger.info("Delete document action completed for document_id=%s", document_id)
    return DocumentDeleteResponse(document_id=document_id, deleted=deleted)
