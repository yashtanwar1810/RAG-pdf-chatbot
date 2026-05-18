from app.rag.chains.rag_chain import RagChain


class ChatService:
    def __init__(self, chain: RagChain) -> None:
        self.chain = chain

    def ask(self, document_id: str, question: str, top_k: int) -> tuple[str, list[dict]]:
        return self.chain.answer(document_id=document_id, question=question, top_k=top_k)

    async def ask_async(self, document_id: str, question: str, top_k: int) -> tuple[str, list[dict]]:
        return await self.chain.answer_async(document_id=document_id, question=question, top_k=top_k)
