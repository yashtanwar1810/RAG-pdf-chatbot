import logging
from pathlib import Path

import cloudinary
import cloudinary.uploader

from app.core.config import get_settings
from app.db.database import StoredDocument, db

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._configure_cloudinary()

    def _configure_cloudinary(self) -> None:
        if (
            self.settings.cloudinary_cloud_name
            and self.settings.cloudinary_api_key
            and self.settings.cloudinary_api_secret
        ):
            cloudinary.config(
                cloud_name=self.settings.cloudinary_cloud_name,
                api_key=self.settings.cloudinary_api_key,
                api_secret=self.settings.cloudinary_api_secret,
                secure=True,
            )

    def upload_pdf(self, filename: str, raw_bytes: bytes) -> str:
        if self.settings.storage_backend == "cloudinary":
            return self._upload_cloudinary(filename, raw_bytes)
        if self.settings.storage_backend == "local":
            return self._upload_local(filename, raw_bytes)
        raise ValueError("STORAGE_BACKEND must be one of: 'cloudinary', or 'local'.")

    def _upload_cloudinary(self, filename: str, raw_bytes: bytes) -> str:
        if not (
            self.settings.cloudinary_cloud_name
            and self.settings.cloudinary_api_key
            and self.settings.cloudinary_api_secret
        ):
            raise ValueError("Cloudinary credentials are missing.")
        result = cloudinary.uploader.upload(
            raw_bytes,
            resource_type="raw",
            public_id=f"pdfs/{filename}",
            overwrite=True,
            filename=filename,
            use_filename=True,
        )
        return str(result["secure_url"])

    
    def _upload_local(self, filename: str, raw_bytes: bytes) -> str:
        local_dir = Path(self.settings.local_storage_dir)
        local_dir.mkdir(parents=True, exist_ok=True)
        path = local_dir / filename
        path.write_bytes(raw_bytes)
        return str(path.resolve())

    def save_document(self, document_id: str, filename: str, file_url: str, chunks: list[str]) -> None:
        db.upsert_document(
            StoredDocument(
                document_id=document_id,
                filename=filename,
                file_url=file_url,
                chunks=chunks,
            )
        )

    def list_documents(self) -> list[StoredDocument]:
        return db.list_documents()

    def get_document(self, document_id: str) -> StoredDocument | None:
        return db.get_document(document_id)

    def delete_document(self, document_id: str) -> bool:
        doc = db.get_document(document_id)
        if doc and doc.file_url:
            try:
                self.delete_pdf(doc.file_url, doc.filename)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to delete remote PDF for %s: %s", document_id, exc)
        return db.delete_document(document_id)

    def delete_pdf(self, file_url: str, filename: str) -> None:
        if self.settings.storage_backend == "cloudinary":
            public_id = f"pdfs/{filename.rsplit('.', 1)[0]}"
            cloudinary.uploader.destroy(public_id, resource_type="raw")
            return
        if self.settings.storage_backend == "local":
            path = Path(file_url)
            if path.exists():
                path.unlink()
