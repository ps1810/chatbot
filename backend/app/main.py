from fastapi import FastAPI
from app.api.v1 import chat
from fastapi.middleware.cors import CORSMiddleware
from app.core.lifecycle import lifespan
from app.middleware.timeout import TimeoutMiddleware
from app.core.config import settings

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(TimeoutMiddleware, timeout=settings.request_timeout)

app.include_router(chat.router)