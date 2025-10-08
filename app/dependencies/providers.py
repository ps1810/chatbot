from app.core.model_context import model_context
from app.services.chat_service import ChatService

def get_chat_service():
    return model_context.get_service()