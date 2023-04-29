"""Main module for the Flock Orchestrator server."""

from fastapi import FastAPI
from flock_models.builder import ResourceBuilder
from flock_resource_store import ResourceStoreFactory

from server.apis.flock_api import get_router

app = FastAPI(
    title="Flock",
    description="Flock Orchestrator",
    version="0.0.1",
)
resource_store = ResourceStoreFactory.get_resource_store()
resource_builder = ResourceBuilder(resource_store=resource_store)

router = get_router(resource_store=resource_store, resource_builder=resource_builder)
app.include_router(router)
# app.add_middleware(
#     middleware=validate,
#     dispatch=app.router.routes[0].endpoint,
# )
