from pydantic import BaseModel
from typing import List, Optional, Dict

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict]] = []

class ChatResponse(BaseModel):
    response: str