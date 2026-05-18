import asyncio

from google import genai

from app.core.config import get_settings


class EmbeddingService:
    def __init__(self) -> None:
        settings = get_settings()
        provider = settings.llm_provider.lower()

        if provider == "gemini":
            if not settings.google_api_key:
                raise ValueError("GOOGLE_API_KEY is required for Gemini embedding generation.")
            self.client = genai.Client(api_key=settings.google_api_key)
            self.embedding_model = self._normalize_gemini_embedding_model(settings.embedding_model)
        else:
            raise ValueError(f"Unsupported llm_provider '{settings.llm_provider}'. Use 'gemini' or 'openai'.")
        self.provider = provider

    @staticmethod
    def _normalize_gemini_embedding_model(model_name: str) -> str:
        normalized = model_name.strip()
        if normalized.startswith("models/"):
            normalized = normalized.split("models/", 1)[1]

        # Known invalid/legacy naming patterns seen in user envs.
        if normalized in {"gemini-embedding-004", "text-embedding-004"}:
            return "gemini-embedding-001"
        return normalized

    def embed_text(self, text: str) -> list[float]:
        if self.provider == "gemini":
            response = self.client.models.embed_content(
                model=self.embedding_model,
                contents=text,
            )
            if not response.embeddings:
                return []
            embedding = response.embeddings[0]
            values = getattr(embedding, "values", None)
            if values is None:
                return []
            return [float(v) for v in values]
        return self.client.embed_query(text)

    async def embed_text_async(self, text: str) -> list[float]:
        if self.provider == "gemini":
            response = await self.client.aio.models.embed_content(
                model=self.embedding_model,
                contents=text,
            )
            if not response.embeddings:
                return []
            embedding = response.embeddings[0]
            values = getattr(embedding, "values", None)
            if values is None:
                return []
            return [float(v) for v in values]
        return await asyncio.to_thread(self.embed_text, text)
