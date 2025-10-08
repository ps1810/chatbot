import threading
from typing import Optional
from app.infrastructure.model_loader import ModelLoader
from app.services.chat_service import ChatService
from app.core.periodic_cleanup import PeriodicCleanup
import asyncio
from app.core.config import settings

class ModelContext:
    def __init__(self):
        self._lock = threading.Lock()
        self._model: Optional[object] = None
        self._tokenizer: Optional[object] = None
        self._initialized: bool = False
        self._chat_service: Optional[ChatService] = None
        self._cleanup_task: Optional[PeriodicCleanup] = None

    async def initialize(self, model_name: str) -> None:
        with self._lock:
            if not self._initialized:
                loader = ModelLoader(model_name)
                components = loader.load()
                self._model = components["model"]
                self._tokenizer = components["tokenizer"]
                self._chat_service = ChatService(self._model, self._tokenizer)
                self._cleanup_task = PeriodicCleanup(
                    self._chat_service, 
                    interval_seconds=settings.cleanup_interval_seconds
                )
                self._cleanup_task.start()
                self._initialized = True
                
    async def cleanup(self) -> None:
        with self._lock:
            if not self._initialized:
                return

            if self._cleanup_task:
                self._cleanup_task.stop()
                self._cleanup_task = None

            if self._chat_service:
                self._chat_service.clear_memory()
            
            self._model = None
            self._tokenizer = None
            self._initialized = False
            self._chat_service = None

    def get_service(self) -> ChatService:
        with self._lock:
            if not self._initialized or self._chat_service is None:
                raise RuntimeError("Model not initialized")
            return self._chat_service

model_context = ModelContext()
    