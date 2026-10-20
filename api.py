"""FastAPI Application for Bereket Abera's Digital Twin.

Provides REST and Server-Sent Events (SSE) streaming endpoints with
IP-based rate limiting, history windowing, and input length protection
to keep AI credits and costs strictly managed.
"""

import json
import os
from typing import AsyncGenerator, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.requests import Request

from agent import run_twin, stream_twin

# -----------------------------------------------------------------------------
# Rate Limiting Configuration (Per IP)
# -----------------------------------------------------------------------------
# Default to 10 requests per minute per IP address to block scrapers & spammers.
# Can be customized via the RATE_LIMIT environment variable (e.g. "5/minute").
DEFAULT_RATE_LIMIT = os.getenv("RATE_LIMIT", "10/minute")

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[DEFAULT_RATE_LIMIT],
)

app = FastAPI(
    title="Bereket Abera · Digital Twin API",
    description="Headless REST & Streaming API powering Bereket Abera's AI Digital Twin.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# -----------------------------------------------------------------------------
# CORS Configuration
# -----------------------------------------------------------------------------
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Request & Response Schemas
# -----------------------------------------------------------------------------
class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message author: 'user' or 'assistant'.")
    # Enforce maximum character length to stop pasted textbook prompt attacks
    content: str = Field(..., max_length=1000, description="The content of the message (max 1000 characters).")


class ChatRequest(BaseModel):
    """Flexible request model supporting both chat history lists and single message format."""
    message: Optional[str] = Field(None, max_length=1000, description="The latest user message string.")
    history: Optional[List[ChatMessage]] = Field(default=[], description="Previous conversation turns.")
    messages: Optional[List[ChatMessage]] = Field(
        None,
        description="Full list of messages in standard format: [{'role': 'user', 'content': '...'}]",
    )

    def to_messages_list(self) -> List[dict]:
        """Normalizes and trims conversation history to prevent quadratic token growth."""
        raw_list: List[dict] = []
        if self.messages:
            raw_list = [{"role": m.role, "content": m.content} for m in self.messages]
        else:
            if self.history:
                for turn in self.history:
                    raw_list.append({"role": turn.role, "content": turn.content})
            if self.message:
                raw_list.append({"role": "user", "content": self.message})

        # Keep only the last 6 messages (3 conversation turns) to cap context token usage
        trimmed = raw_list[-6:] if len(raw_list) > 6 else raw_list

        for msg in trimmed:
            if len(msg["content"]) > 1000:
                msg["content"] = msg["content"][:1000]

        return trimmed


class ChatResponse(BaseModel):
    response: str = Field(..., description="Complete response text from the digital twin.")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    rate_limit: str


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@app.get("/", tags=["General"])
def root():
    return {
        "message": "Bereket Abera Digital Twin API is online.",
        "docs": "/docs",
        "health": "/health",
        "rate_limit": DEFAULT_RATE_LIMIT,
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
def health_check():
    return HealthResponse(
        status="ok",
        service="digital-twin-backend",
        version="1.0.0",
        rate_limit=DEFAULT_RATE_LIMIT,
    )


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
@limiter.limit(DEFAULT_RATE_LIMIT)
async def chat_endpoint(request: Request, payload: ChatRequest):
    """Standard non-streaming JSON endpoint protected by IP rate limiting."""
    messages = payload.to_messages_list()
    if not messages:
        raise HTTPException(status_code=400, detail="No message or messages provided.")

    try:
        reply = await run_twin(messages)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Twin inference error: {e}")


@app.post("/api/chat/stream", tags=["Chat"])
@limiter.limit(DEFAULT_RATE_LIMIT)
async def chat_stream_endpoint(request: Request, payload: ChatRequest):
    """Server-Sent Events (SSE) streaming endpoint protected by IP rate limiting."""
    messages = payload.to_messages_list()
    if not messages:
        raise HTTPException(status_code=400, detail="No message or messages provided.")

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            async for chunk in stream_twin(messages):
                yield f"data: {json.dumps({'text': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# -----------------------------------------------------------------------------
# Execution Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"[API] Starting Digital Twin FastAPI server on http://{host}:{port} with rate limit {DEFAULT_RATE_LIMIT}")
    uvicorn.run("api:app", host=host, port=port, reload=True)
