import asyncio
from typing import Any

from app.services.storage_service import StorageService


class DocumentService:
    def __init__(self, storage: StorageService, vector_store: Any) -> None:
        self.storage = storage
        self.vector_store = vector_store

    def list_documents(self) -> list[dict]:
        return [
            {
                "document_id": doc.document_id,
                "filename": doc.filename,
                "file_url": doc.file_url,
                "chunk_count": len(doc.chunks),
            }
            for doc in self.storage.list_documents()
        ]

    def delete_document(self, document_id: str) -> bool:
        self.vector_store.delete_namespace(document_id)
        return self.storage.delete_document(document_id)

    async def list_documents_async(self) -> list[dict]:
        return await asyncio.to_thread(self.list_documents)

    async def delete_document_async(self, document_id: str) -> bool:
        await self.vector_store.delete_namespace_async(document_id)
        return await asyncio.to_thread(self.storage.delete_document, document_id)
