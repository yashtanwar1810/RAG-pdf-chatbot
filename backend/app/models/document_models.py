from pydantic import BaseModel


class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    file_url: str
    chunk_count: int


class DocumentListResponse(BaseModel):
    items: list[DocumentInfo]


class DocumentDeleteResponse(BaseModel):
    document_id: str
    deleted: bool
