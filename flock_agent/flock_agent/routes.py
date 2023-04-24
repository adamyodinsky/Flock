import os
import signal
import time
from typing import Union

from fastapi import APIRouter, Depends

from models import (
    AgentRequest,
    AgentResponse,
    ErrorResponse,
    ShutdownRequest,
)

router = APIRouter()


async def shut_down(timeout: int = 5):
    time.sleep(timeout)
    os.kill(os.getpid(), signal.SIGTERM)


def create_agent_routes(agent):
    @router.post("/agent")
    async def agent_endpoint(
        req: AgentRequest, agent=Depends(lambda: agent)
    ) -> Union[AgentResponse, ErrorResponse]:
        response = agent.get_response(req.msg)
        return AgentResponse(data=str(response))

    # route for graceful shutdown
    @router.get("/shutdown")
    async def shutdown_endpoint() -> ErrorResponse:
        print("Shutting down...")
        shut_down(10)
        response = ShutdownRequest(countdown=10, message="Shutting down...")
        return response

    return router
