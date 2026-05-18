from app.rag.embeddings.embedding_service import EmbeddingService
from app.rag.vectorstores.pinecone_store import PineconeStore, VectorRecord


class Retriever:
    def __init__(self, store: PineconeStore, embedder: EmbeddingService) -> None:
        self.store = store
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int, namespace: str) -> list[tuple[VectorRecord, float]]:
        qvec = self.embedder.embed_text(query)
        return self.store.query(qvec, top_k, namespace=namespace)

    async def retrieve_async(self, query: str, top_k: int, namespace: str) -> list[tuple[VectorRecord, float]]:
        qvec = await self.embedder.embed_text_async(query)
        return await self.store.query_async(qvec, top_k, namespace=namespace)
