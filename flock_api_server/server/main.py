"""Main module for the Flock Orchestrator server."""

from fastapi import FastAPI
from flock_resource_store.mongo import MongoResourceStore

from server.apis.flock_api import get_router

app = FastAPI(
    title="Flock",
    description="Flock Orchestrator",
    version="0.0.1",
)
resource_store = MongoResourceStore(
    collection_name="resources",
    host="localhost",
    db_name="flock",
    port=27017,
)

router = get_router(resource_store=resource_store)
app.include_router(router)
