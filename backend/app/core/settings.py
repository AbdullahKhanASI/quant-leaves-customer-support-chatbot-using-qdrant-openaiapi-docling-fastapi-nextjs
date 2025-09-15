"""Application configuration."""
from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Central application settings for Sprint 0 scaffolding."""

    environment: Literal["local", "staging", "production"] = "local"
    database_url: AnyUrl | None = None
    openai_api_key: str | None = None
    openai_api_base: AnyUrl | None = None
    openai_chat_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-large"
    vector_collection: str = "quantleaves_support_corpus"
    vector_table_name: str = "document_embeddings"
    chunk_size: int = 800
    chunk_overlap: int = 120
    ingestion_batch_size: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
