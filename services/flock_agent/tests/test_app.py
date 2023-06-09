from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from flock_agent.agent import FlockAgent
from flock_agent.models import (
    AgentRequest,
)  # AgentResponse,; ErrorResponse,; ShutdownRequest,
from flock_agent.routes import create_agent_routes


def create_test_app():
    """Create test app with agent routes"""
    # Initialize agent object with the test configuration manifest
    flock_agent = MagicMock(spec=FlockAgent)
    flock_agent.get_response.return_value = "test"

    # Create FastAPI app and include the agent routes
    app = FastAPI()
    routes = create_agent_routes(flock_agent)
    app.include_router(routes)

    return app


client = TestClient(create_test_app())


def test_agent_endpoint():
    """Test agent endpoint"""
    request = AgentRequest(msg="test")
    response = client.post("/agent", json=request.dict())

    assert response.json()["status_code"] == 200
    assert response.json()["data"] == "test"


# Add more tests as needed
