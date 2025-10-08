from contextlib import asynccontextmanager
from app.core.model_context import model_context
from app.core.config import settings
from fastapi import FastAPI
from app.core.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Initializing model: {settings.model_name}")
    await model_context.initialize(settings.model_name)
    yield
    await model_context.cleanup()
    logger.info("Model cleaned up")
