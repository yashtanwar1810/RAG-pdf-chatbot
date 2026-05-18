import logging

from fastapi import APIRouter, Depends

from app.api.deps import get_chat_service
from app.core.config import get_settings
from app.core.security import verify_api_key
from app.models.chat_models import ChatRequest, ChatResponse, SourceChunk
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"], dependencies=[Depends(verify_api_key)])
logger = logging.getLogger(__name__)


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    settings = get_settings()
    top_k = payload.top_k or settings.top_k
    logger.info("Chat action started for document_id=%s, top_k=%s", payload.document_id, top_k)
    answer, sources = await chat_service.ask_async(payload.document_id, payload.question, top_k=top_k)
    logger.info("Chat action completed for document_id=%s with %s sources", payload.document_id, len(sources))
    return ChatResponse(
        answer=answer,
        sources=[SourceChunk(**src) for src in sources],
    )
