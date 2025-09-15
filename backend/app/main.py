"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, health, ingest
from app.core.logging import configure_logging

configure_logging()
app = FastAPI(title="QuantLeaves Support RAG", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(ingest.router)


@app.get("/", summary="Service metadata")
async def root() -> dict:
    """Basic metadata endpoint to verify service bootstrap."""
    return {"service": "quantleaves-support-rag", "status": "active"}
