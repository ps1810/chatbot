from fastapi import APIRouter, Request, Depends
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.chat_service import ChatService
from app.dependencies.providers import get_chat_service
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatMessage, chat_service: ChatService = Depends(get_chat_service)):
    response = chat_service.chat(request.message, request.history)
    return ChatResponse(response=response)

@router.get("/health")
async def health(chat_service: ChatService = Depends(get_chat_service)):
    logger.info("Health check")
    return {"status": "healthy", "model_loaded": chat_service.model is not None}
