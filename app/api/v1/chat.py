from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.chat_service import ChatService
from app.dependencies.providers import get_chat_service
from app.core.logger import get_logger
import asyncio

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatMessage, chat_service: ChatService = Depends(get_chat_service)):
    try:
        if not request.message or not request.message.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Message cannot be empty"
                )
        response = await asyncio.to_thread( 
            chat_service.chat, 
            request.message, 
            request.history
        )
        return ChatResponse(response=response)
    except RuntimeError as e:
        logger.error(f"Service error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/health")
async def health(chat_service: ChatService = Depends(get_chat_service)):
    logger.info("Health check")
    return {"status": "healthy", "model_loaded": chat_service.model is not None}
