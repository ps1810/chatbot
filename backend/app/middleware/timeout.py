from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio

class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: int = 60):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(
                call_next(request), 
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Request timeout")