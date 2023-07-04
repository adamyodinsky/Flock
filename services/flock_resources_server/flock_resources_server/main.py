"""Main module for the Flock Orchestrator server."""

import logging
import os
import sys

import click
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_builder import ResourceBuilder
from flock_common import EnvVarNotSetError, check_env_vars, init_logging
from flock_resource_store import ResourceStoreFactory
from uvicorn import run

from flock_resources_server.api.resource_api import get_router

init_logging(
    destination=os.environ.get("LOG_DESTINATION", "console"),
    level=os.environ.get("LOG_LEVEL", "INFO"),
)


@click.group()
def cli():
    """Flock Resources API Server CLI"""


@cli.command(
    help="Run the Resources API Server.",
)
@click.option(
    "--host",
    default=os.environ.get("HOST", "127.0.0.1"),
    help="The host address to bind the server to.",
)
@click.option(
    "--port",
    default=os.environ.get("PORT", 9001),
    type=int,
    help="The port the server should listen on.",
)
def run_server(host, port):
    """Run the Resources API Server."""

    load_dotenv(find_dotenv(os.environ.get("ENV_FILE", ".env")))
    check_env_vars([], [])

    app = FastAPI(
        title="Flock",
        description="Flock Resources API Server",
        version="0.0.1",
    )
    resource_store = ResourceStoreFactory.get_resource_store()
    resource_builder = ResourceBuilder(resource_store=resource_store)

    router = get_router(
        resource_store=resource_store, resource_builder=resource_builder
    )
    app.include_router(router)
    logging.info("Starting server...")
    logging.info("/docs (GET) (http://%s:%s/docs)", host, port)
    logging.info("/redoc (GET) (http://%s:%s/redoc)", host, port)
    logging.info("/openapi.json (GET) (http://%s:%s/openapi.json)", host, port)
    run(
        app, host=host, port=port, log_level=os.environ.get("LOG_LEVEL", "info").lower()
    )


cli.add_command(run_observer)


if __name__ == "__main__":
    try:
        cli()
    except EnvVarNotSetError as e:
        logging.error(str(e))
        sys.exit(1)
