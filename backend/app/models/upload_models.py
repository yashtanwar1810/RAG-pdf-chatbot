from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    document_id: str = Field(..., description="Generated document id")
    filename: str
    chunks_created: int
    status: str
    message: str
