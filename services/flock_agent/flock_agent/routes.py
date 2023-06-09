"""Routes for the agent."""

import os
import signal
import time
from typing import Union

from fastapi import APIRouter, Depends, WebSocket

from flock_agent.agent import FlockAgent
from flock_agent.models import (
    AgentRequest,
    AgentResponse,
    ErrorResponse,
    ShutdownRequest,
)

router = APIRouter()


async def shut_down(timeout: int = 5):
    """Shut down the server gracefully."""

    time.sleep(timeout)
    os.kill(os.getpid(), signal.SIGTERM)


def create_agent_routes(agent):
    """Create routes for the agent."""

    @router.post("/agent")
    async def agent_endpoint(
        req: AgentRequest, agent: FlockAgent = Depends(lambda: agent)
    ) -> Union[AgentResponse, ErrorResponse]:
        response = agent.get_response(req.msg)
        return AgentResponse(data=str(response))

    @router.websocket("/agent_ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")

    # route for graceful shutdown
    @router.get("/shutdown")
    async def shutdown_endpoint():
        print("Shutting down...")
        _ = shut_down(10)
        response = ShutdownRequest(countdown=10, message="Shutting down...")
        return response

    return router
