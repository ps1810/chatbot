import threading
from typing import Optional
from app.infrastructure.model_loader import ModelLoader
from app.services.chat_service import ChatService


class ModelContext:
    def __init__(self):
        self._lock = threading.Lock()
        self._model: Optional[object] = None
        self._tokenizer: Optional[object] = None
        self._initialized: bool = False

    def initialize(self, model_name: str) -> None:
        with self._lock:
            if not self._initialized:
                loader = ModelLoader(model_name)
                components = loader.load()
                self._model = components["model"]
                self._tokenizer = components["tokenizer"]
                self._initialized = True
                
    def cleanup(self) -> None:
        with self._lock:
            if self._initialized:
                self._model = None
                self._tokenizer = None
                self._initialized = False

    def get_service(self) -> ChatService:
        with self._lock:
            if not self._initialized:
                raise RuntimeError("Model not initialized")
            
            return ChatService(self._model, self._tokenizer)

model_context = ModelContext()
    