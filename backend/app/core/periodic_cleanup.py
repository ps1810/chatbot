import asyncio
from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)


class PeriodicCleanup:
    """Periodic cleanup task"""
    
    def __init__(self, chat_service, interval_seconds: int = settings.cleanup_interval_seconds):
        self.chat_service = chat_service
        self.interval = interval_seconds
        self.task = None
        
    def start(self):
        """Start periodic cleanup task"""
        self.task = asyncio.create_task(self._cleanup_loop())
        logger.info(f"Started periodic cleanup (every {self.interval}s)")
        
    def stop(self):
        """Stop periodic cleanup task"""
        if self.task:
            self.task.cancel()
            logger.info("Stopped periodic cleanup")
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                await asyncio.sleep(self.interval)
                
                # Perform cleanup
                self.chat_service.clear_memory()
                
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
