import asyncio

from google import genai
from langchain_openai import ChatOpenAI

from app.core.config import get_settings
from app.rag.prompts.rag_prompt import build_rag_prompt
from app.rag.retrievers.retriever import Retriever


class RagChain:
    def __init__(self, retriever: Retriever) -> None:
        self.retriever = retriever
        settings = get_settings()
        provider = settings.llm_provider.lower()
        self.provider = provider

        if provider == "gemini":
            if not settings.google_api_key:
                raise ValueError("GOOGLE_API_KEY is required for Gemini chat generation.")
            self.client = genai.Client(api_key=settings.google_api_key)
            self.model_name = settings.model_name
        elif provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for OpenAI chat generation.")
            self.llm = ChatOpenAI(
                model=settings.model_name,
                api_key=settings.openai_api_key,
                temperature=0,
            )
        else:
            raise ValueError(f"Unsupported llm_provider '{settings.llm_provider}'. Use 'gemini' or 'openai'.")

    def answer(self, document_id: str, question: str, top_k: int) -> tuple[str, list[dict]]:
        hits = self.retriever.retrieve(question, top_k=top_k, namespace=document_id)
        context_chunks = [item.text for item, _ in hits]
        if not hits:
            return "I could not find that information in the document.", []
        prompt = build_rag_prompt(question, context_chunks)
        if self.provider == "gemini":
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            answer = str(response.text or "").strip()
        else:
            response = self.llm.invoke(prompt)
            answer = str(response.content).strip()
        sources = [
            {
                "document_id": rec.metadata["document_id"],
                "file_name": rec.metadata["file_name"],
                "page": int(rec.metadata["page"]),
                "chunk_id": rec.metadata["chunk_id"],
                "text": rec.text,
                "score": float(score),
            }
            for rec, score in hits
        ]
        return answer, sources

    async def answer_async(self, document_id: str, question: str, top_k: int) -> tuple[str, list[dict]]:
        hits = await self.retriever.retrieve_async(question, top_k=top_k, namespace=document_id)
        context_chunks = [item.text for item, _ in hits]
        if not hits:
            return "I could not find that information in the document.", []
        prompt = build_rag_prompt(question, context_chunks)
        if self.provider == "gemini":
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt,
            )
            answer = str(response.text or "").strip()
        else:
            response = await asyncio.to_thread(self.llm.invoke, prompt)
            answer = str(response.content).strip()
        sources = [
            {
                "document_id": rec.metadata["document_id"],
                "file_name": rec.metadata["file_name"],
                "page": int(rec.metadata["page"]),
                "chunk_id": rec.metadata["chunk_id"],
                "text": rec.text,
                "score": float(score),
            }
            for rec, score in hits
        ]
        return answer, sources
