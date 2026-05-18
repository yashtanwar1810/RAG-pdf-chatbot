import asyncio
from dataclasses import dataclass

from pinecone import Pinecone

@dataclass
class VectorRecord:
    vector_id: str
    values: list[float]
    text: str
    metadata: dict[str, str | int]
    namespace: str


class PineconeStore:
    def __init__(self) -> None:
        from app.core.config import get_settings

        settings = get_settings()
        if not settings.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY is required for vector store operations.")
        if not settings.pinecone_index:
            raise ValueError("PINECONE_INDEX is required for vector store operations.")

        client = Pinecone(api_key=settings.pinecone_api_key)
        if settings.pinecone_host:
            self.index = client.Index(host=settings.pinecone_host)
        else:
            self.index = client.Index(settings.pinecone_index)

    def upsert(self, record: VectorRecord) -> None:
        self.index.upsert(
            vectors=[
                {
                    "id": record.vector_id,
                    "values": record.values,
                    "metadata": {**record.metadata, "text": record.text},
                }
            ],
            namespace=record.namespace,
        )

    async def upsert_async(self, record: VectorRecord) -> None:
        await asyncio.to_thread(self.upsert, record)

    def query(self, query_vector: list[float], top_k: int, namespace: str) -> list[tuple[VectorRecord, float]]:
        response = self.index.query(
            vector=query_vector,
            top_k=top_k,
            namespace=namespace,
            include_metadata=True,
            include_values=False,
        )
        hits: list[tuple[VectorRecord, float]] = []
        for match in response.matches or []:
            metadata = match.metadata or {}
            text = str(metadata.get("text", ""))
            rec = VectorRecord(
                vector_id=match.id,
                values=[],
                text=text,
                metadata={
                    "document_id": str(metadata.get("document_id", "")),
                    "file_name": str(metadata.get("file_name", "")),
                    "page": int(metadata.get("page", 1)),
                    "chunk_id": str(metadata.get("chunk_id", match.id)),
                },
                namespace=namespace,
            )
            hits.append((rec, float(match.score or 0.0)))
        return hits

    async def query_async(self, query_vector: list[float], top_k: int, namespace: str) -> list[tuple[VectorRecord, float]]:
        return await asyncio.to_thread(self.query, query_vector, top_k, namespace)

    def delete_namespace(self, namespace: str) -> int:
        self.index.delete(delete_all=True, namespace=namespace)
        return 1

    async def delete_namespace_async(self, namespace: str) -> int:
        return await asyncio.to_thread(self.delete_namespace, namespace)
