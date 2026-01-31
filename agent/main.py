"""
Second Brain Agent - FastAPI application with AG-UI streaming endpoint.

This agent transforms Markdown research documents into generative UI dashboards
using Pydantic AI and the AG-UI protocol.
"""

import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from ag_ui_protocol import AGUIAdapter

# Load environment variables
load_dotenv()

# Import the Pydantic AI agent
from agent import agent, AgentState, create_agent

# Configuration
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3010,http://localhost:3011,http://localhost:3012,http://localhost:3000,http://localhost:8080"
).split(",")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4")


# Pydantic models
class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str
    agent_ready: bool


class AgentRequest(BaseModel):
    """AG-UI agent request model."""

    markdown: str
    user_id: str | None = None


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global agent

    print(f"🚀 Second Brain Agent starting on port {BACKEND_PORT}")
    print(f"📡 AG-UI endpoint: http://localhost:{BACKEND_PORT}/ag-ui/stream")
    print(f"🔑 OpenRouter model: {OPENROUTER_MODEL}")

    if not OPENROUTER_API_KEY:
        print("⚠️  WARNING: OPENROUTER_API_KEY not set in environment")
    else:
        # Re-initialize agent if it wasn't initialized during import
        if agent is None:
            try:
                agent = create_agent()
                print("✅ Pydantic AI agent initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize agent: {e}")

    yield

    print("👋 Second Brain Agent shutting down")


# Create FastAPI app
app = FastAPI(
    title="Second Brain Agent",
    description="Pydantic AI agent for transforming Markdown into generative UI dashboards",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=False,  # Must be False when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify the agent is running."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        agent_ready=OPENROUTER_API_KEY is not None,
    )


# AG-UI streaming endpoint
@app.post("/ag-ui/stream")
async def ag_ui_stream(request: AgentRequest):
    """
    AG-UI streaming endpoint for generative UI using AGUIAdapter.

    This endpoint receives Markdown content and streams back AG-UI protocol
    messages containing the generated dashboard components.

    Protocol flow:
    1. Client sends POST with { markdown: "...", user_id: "..." }
    2. AGUIAdapter wraps the Pydantic AI agent
    3. Agent analyzes content and determines optimal layout
    4. AGUIAdapter streams AG-UI messages with component definitions
    5. Client renders components in real-time using A2UI

    Returns:
        StreamingResponse with text/event-stream content type
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY not configured. Please set it in .env file.",
        )

    if not request.markdown or not request.markdown.strip():
        raise HTTPException(
            status_code=400,
            detail="Markdown content is required and cannot be empty.",
        )

    async def event_generator() -> AsyncGenerator[str, None]:
        """
        Generate AG-UI protocol events using AGUIAdapter.

        The AGUIAdapter handles the streaming protocol and wraps our Pydantic AI
        agent to emit properly formatted AG-UI messages.
        """
        # Create agent state with the markdown content
        state = AgentState(document_content=request.markdown)

        # Create AGUIAdapter instance for streaming
        adapter = AGUIAdapter(agent)

        # Use AGUIAdapter.run_stream() to handle SSE streaming
        # This yields properly formatted SSE events
        async for event in adapter.run_stream(
            prompt="Analyze this markdown document and extract key components for dashboard creation.",
            deps=state,
        ):
            yield event

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Second Brain Agent",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "ag_ui_stream": "/ag-ui/stream (POST)",
        },
        "documentation": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=BACKEND_PORT,
        reload=True,
        log_level="info",
    )
