from fastapi import FastAPI
from app.api.v1 import chat
from fastapi.middleware.cors import CORSMiddleware
from app.core.lifecycle import lifespan

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(chat.router)