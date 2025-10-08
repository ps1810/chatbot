from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: Optional[List[Dict]] = Field(default_factory=list)

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or whitespace')
        return v.strip()
    
    @field_validator('history')
    @classmethod
    def validate_history(cls, v):
        for msg in v:
            if 'role' not in msg or 'content' not in msg:
                raise ValueError('History messages must have role and content')
            if msg['role'] not in ['user', 'assistant']:
                raise ValueError('Invalid role in history')
        return v

class ChatResponse(BaseModel):
    response: str