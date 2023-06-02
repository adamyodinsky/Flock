from fastapi import APIRouter, FastAPI, Response
from flock_common.queue_client import QueueClient

app = FastAPI()
router = APIRouter()


def create_routes(queue_client: QueueClient = NotImplemented):
    """Create routes for the agent."""

    @router.get("/")
    async def health_check():
        return Response(status_code=200, content="OK")

    @router.on_event("shutdown")
    async def shutdown_event():
        queue_client.close()

    return router
