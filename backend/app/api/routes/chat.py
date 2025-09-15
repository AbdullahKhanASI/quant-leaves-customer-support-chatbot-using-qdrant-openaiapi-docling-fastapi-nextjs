"""Chat inference routes."""
from fastapi import APIRouter, Depends

from app.api.deps import get_chat_service
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, summary="Run hybrid RAG chat pipeline")
async def chat_endpoint(payload: ChatRequest, service: ChatService = Depends(get_chat_service)) -> ChatResponse:
    """Execute the hybrid retrieval + generation pipeline for a user query."""
    return await service.answer(payload)
