from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    document_id: str = Field(..., min_length=3)
    question: str = Field(..., min_length=3)
    top_k: int | None = Field(default=None, ge=1, le=20)


class SourceChunk(BaseModel):
    document_id: str
    file_name: str
    page: int
    chunk_id: str
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
