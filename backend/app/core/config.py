from functools import lru_cache
from pydantic import Field
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


class Settings(BaseSettings):
    app_name: str = "Backend RAG API"
    app_env: str = "dev"
    api_prefix: str = "/api/v1"
    max_upload_size_mb: int = 10
    chunk_size: int = 500
    chunk_overlap: int = 75
    top_k: int = 4
    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    model_name: str = "gemini-2.5-flash"
    embedding_model: str = "gemini-embedding-001"
    pinecone_index: str = "rag-index"
    pinecone_host: str = ""
    pinecone_api_key: str = ""
    openai_api_key: str = ""
    google_api_key: str = ""
    llm_provider: str = "gemini"
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket_name: str = ""
    storage_backend: str = "cloudinary"
    local_storage_dir: str = "uploads"
    require_api_key: bool = False
    app_api_key: str = ""

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: object) -> object:
        if isinstance(value, str):
            raw = value.strip()
            if raw.startswith("["):
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except json.JSONDecodeError:
                    pass
            return [item.strip() for item in raw.split(",") if item.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=(),
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
