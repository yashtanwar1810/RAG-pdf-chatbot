def build_rag_prompt(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    return (
        "You are a helpful PDF assistant.\n\n"
        "Answer ONLY from the provided context.\n\n"
        "If the answer is not found, say: "
        "'I could not find that information in the document.'\n\n"
        f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
    )
