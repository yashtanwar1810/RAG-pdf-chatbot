from functools import lru_cache

from app.rag.chains.rag_chain import RagChain
from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.retrievers.retriever import Retriever
from app.rag.vectorstores.pinecone_store import PineconeStore
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.ingestion_service import IngestionService
from app.services.storage_service import StorageService


@lru_cache
def get_store() -> PineconeStore:
    return PineconeStore()


@lru_cache
def get_embedder() -> EmbeddingService:
    return EmbeddingService()


@lru_cache
def get_storage_service() -> StorageService:
    return StorageService()


@lru_cache
def get_ingestion_service() -> IngestionService:
    return IngestionService(get_store(), get_embedder(), get_storage_service())


@lru_cache
def get_chat_service() -> ChatService:
    retriever = Retriever(get_store(), get_embedder())
    chain = RagChain(retriever)
    return ChatService(chain)


@lru_cache
def get_document_service() -> DocumentService:
    return DocumentService(get_storage_service(), get_store())
