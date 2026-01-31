"""
AG-UI Protocol Adapter - Minimal implementation for streaming A2UI components.

This adapter wraps the Pydantic AI agent to stream components in AG-UI protocol format.
"""

import json
from typing import AsyncGenerator, Any


class AGUIAdapter:
    """
    Adapter for streaming A2UI components via AG-UI protocol.

    This is a minimal implementation that handles Server-Sent Events (SSE)
    streaming for the /ag-ui/stream endpoint.
    """

    def __init__(self, agent=None):
        """
        Initialize the AGUIAdapter.

        Args:
            agent: Optional Pydantic AI agent (not used in orchestrator mode)
        """
        self.agent = agent

    async def run_stream(
        self,
        prompt: str,
        deps: Any = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream AG-UI protocol events.

        This is a placeholder implementation that yields status messages.
        The actual component streaming is handled directly in main.py
        using orchestrate_dashboard().

        Args:
            prompt: The prompt for the agent
            deps: Agent dependencies (AgentState)

        Yields:
            SSE-formatted event strings
        """
        # Status events
        yield f"data: {json.dumps({'type': 'status', 'message': 'Agent initialized'})}\n\n"
        yield f"data: {json.dumps({'type': 'status', 'message': 'Analyzing markdown content...'})}\n\n"
        yield f"data: {json.dumps({'type': 'complete', 'message': 'Dashboard generation complete'})}\n\n"
