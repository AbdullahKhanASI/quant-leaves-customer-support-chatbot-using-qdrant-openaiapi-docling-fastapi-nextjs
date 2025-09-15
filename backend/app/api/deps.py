"""FastAPI dependency factories."""
from functools import lru_cache

from app.services.chat import ChatService
from app.services.ingestion import IngestionService


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService()


@lru_cache
def get_ingestion_service() -> IngestionService:
    return IngestionService()
