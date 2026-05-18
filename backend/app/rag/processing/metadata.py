def build_chunk_metadata(document_id: str, file_name: str, page: int, chunk_index: int) -> dict[str, str | int]:
    return {
        "document_id": document_id,
        "file_name": file_name,
        "page": page,
        "chunk_id": f"{document_id}_chunk_{chunk_index}",
    }
