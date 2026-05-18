from dataclasses import dataclass, field


@dataclass
class StoredDocument:
    document_id: str
    filename: str
    file_url: str = ""
    chunks: list[str] = field(default_factory=list)


class InMemoryDB:
    def __init__(self) -> None:
        self.documents: dict[str, StoredDocument] = {}

    def upsert_document(self, doc: StoredDocument) -> None:
        self.documents[doc.document_id] = doc

    def list_documents(self) -> list[StoredDocument]:
        return list(self.documents.values())

    def get_document(self, document_id: str) -> StoredDocument | None:
        return self.documents.get(document_id)

    def delete_document(self, document_id: str) -> bool:
        if document_id not in self.documents:
            return False
        del self.documents[document_id]
        return True


db = InMemoryDB()
