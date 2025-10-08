from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    app_name: str = "BrainBay Chatbot"

    model_name: str = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
    max_memory_mps: str = "4GB"
    max_memory_cpu: str = "12GB"

    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9

    max_history: int = 3
    
settings = Settings()
    