"""Main module for the Flock Orchestrator server."""

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_common import check_env_vars
from flock_models.builder import ResourceBuilder
from flock_resource_store import ResourceStoreFactory

from server.api.flock_api import get_router

load_dotenv(find_dotenv())
check_env_vars([], [])

app = FastAPI(
    title="Flock",
    description="Flock Orchestrator",
    version="0.0.1",
)
resource_store = ResourceStoreFactory.get_resource_store()
resource_builder = ResourceBuilder(resource_store=resource_store)

router = get_router(resource_store=resource_store, resource_builder=resource_builder)
app.include_router(router)
