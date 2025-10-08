from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):

    app_name: str = "BrainBay Chatbot"
    environment: str = "development"

    model_name: str = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
    max_memory_mps: str = "4GB"
    max_memory_cpu: str = "8GB"

    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9

    max_history: int = 3

    cors_origins: List[str] = ["http://localhost:3000"]
    request_timeout: int = 60
    cleanup_interval_seconds: int = 60
    
settings = Settings()
    