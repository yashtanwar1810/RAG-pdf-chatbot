import asyncio
import logging

from app.core.config import get_settings
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.loaders.pdf_loader import load_pdf_text
from app.rag.processing.chunker import chunk_text
from app.rag.processing.cleaner import clean_text
from app.rag.processing.metadata import build_chunk_metadata
from app.rag.vectorstores.pinecone_store import PineconeStore, VectorRecord
from app.services.storage_service import StorageService
from app.utils.file_utils import safe_filename
from app.utils.helpers import new_id

logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(self, store: PineconeStore, embedder: EmbeddingService, storage: StorageService) -> None:
        self.store = store
        self.embedder = embedder
        self.storage = storage

    def ingest_file(self, filename: str, raw_bytes: bytes) -> tuple[str, int]:
        settings = get_settings()
        document_id = new_id("doc")
        text = load_pdf_text(raw_bytes, filename)
        text = clean_text(text)
        if not text.strip():
            raise ValueError("No extractable text found in PDF.")
        chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
        if not chunks:
            raise ValueError("Chunk generation failed for document.")
        safe_name = safe_filename(filename)
        file_url = self.storage.upload_pdf(safe_name, raw_bytes)

        for idx, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            metadata = build_chunk_metadata(document_id, safe_name, page=1, chunk_index=idx)
            vec = self.embedder.embed_text(chunk)
            self.store.upsert(
                VectorRecord(
                    vector_id=metadata["chunk_id"],
                    values=vec,
                    text=chunk,
                    metadata=metadata,
                    namespace=document_id,
                )
            )

        self.storage.save_document(document_id, safe_name, file_url, chunks)
        logger.info("Document %s ingested successfully with %s chunks", document_id, len(chunks))
        return document_id, len(chunks)

    async def ingest_file_async(self, filename: str, raw_bytes: bytes) -> tuple[str, int]:
        settings = get_settings()
        document_id = new_id("doc")
        text = await asyncio.to_thread(load_pdf_text, raw_bytes, filename)
        text = clean_text(text)
        if not text.strip():
            raise ValueError("No extractable text found in PDF.")
        chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
        if not chunks:
            raise ValueError("Chunk generation failed for document.")
        safe_name = safe_filename(filename)
        file_url = await asyncio.to_thread(self.storage.upload_pdf, safe_name, raw_bytes)

        for idx, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            metadata = build_chunk_metadata(document_id, safe_name, page=1, chunk_index=idx)
            vec = await self.embedder.embed_text_async(chunk)
            await self.store.upsert_async(
                VectorRecord(
                    vector_id=metadata["chunk_id"],
                    values=vec,
                    text=chunk,
                    metadata=metadata,
                    namespace=document_id,
                )
            )

        await asyncio.to_thread(self.storage.save_document, document_id, safe_name, file_url, chunks)
        logger.info("Document %s ingested successfully with %s chunks", document_id, len(chunks))
        return document_id, len(chunks)
