"""Main module for the Flock Orchestrator server."""

import logging
import os
import sys

import click
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flock_builder import ResourceBuilder
from flock_common import EnvVarNotSetError, check_env_vars, init_logging
from flock_resource_store import ResourceStoreFactory
from flock_resources_server.api.resource_api import get_router
from flock_schema_store import SchemaStoreFactory
from uvicorn import run

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
    default=os.environ.get("PORT", 9002),
    type=int,
    help="The port the server should listen on.",
)
def run_server(host, port):
    """Run the Resources API Server."""

    load_dotenv(find_dotenv(os.environ.get("ENV_FILE", ".env")))

    required_vars = []
    optional_vars = [
        "HOST",
        "PORT",
        "RESOURCE_STORE_TYPE",
        "RESOURCE_STORE_DB_NAME",
        "RESOURCE_STORE_TABLE_NAME",
        "RESOURCE_STORE_HOST",
        "RESOURCE_STORE_PORT",
        "RESOURCE_STORE_USERNAME",
        "RESOURCE_STORE_PASSWORD",
        "API_PREFIX",
    ]
    check_env_vars(required_vars, optional_vars)

    api_prefix = os.environ.get("API_PREFIX", "resources-server")
    app = FastAPI(
        title="Flock",
        description="Flock Resources API Server",
        version="0.0.1",
        docs_url=f"/{api_prefix}/docs",
        redoc_url=f"/{api_prefix}/redoc",
        openapi_url=f"/{api_prefix}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:5000",
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "https://6411-2a02-14f-3-dd9a-1c72-8cc0-446a-26c6.ngrok-free.app",
        ],
        allow_credentials=True,
        allow_methods=["*"],  # Allow any method
        allow_headers=["*"],  # Allow any header
        # expose_headers=["*"],
    )

    logging.info("Initializing Flock Resource Store")
    resource_store = ResourceStoreFactory.get_resource_store(
        store_type=os.environ.get("RESOURCE_STORE_TYPE", "mongo"),
        db_name=os.environ.get("RESOURCE_STORE_DB_NAME", "flock_db"),
        table_name=os.environ.get("RESOURCE_STORE_TABLE_NAME", "flock_resources"),
        host=os.environ.get("RESOURCE_STORE_HOST", "localhost"),
        port=int(os.environ.get("RESOURCE_STORE_PORT", 27017)),
        username=os.environ.get("RESOURCE_STORE_USERNAME", "root"),
        password=os.environ.get("RESOURCE_STORE_PASSWORD", "password"),
    )
    resource_builder = ResourceBuilder(resource_store=resource_store)

    logging.info("Initializing Flock Schema Store")
    schema_store = SchemaStoreFactory.get_store(
        store_type=os.environ.get("SCHEMA_STORE_TYPE", "mongo"),
        db_name=os.environ.get("SCHEMA_STORE_DB_NAME", "flock_db"),
        table_name=os.environ.get("SCHEMA_STORE_TABLE_NAME", "flock_schema"),
        host=os.environ.get("SCHEMA_STORE_HOST", "localhost"),
        port=int(os.environ.get("SCHEMA_STORE_PORT", 27017)),
        username=os.environ.get("SCHEMA_STORE_USERNAME", "root"),
        password=os.environ.get("SCHEMA_STORE_PASSWORD", "password"),
    )

    router = get_router(
        resource_store=resource_store,
        resource_builder=resource_builder,
        schema_store=schema_store,
        prefix=api_prefix,
    )
    app.include_router(router)
    logging.info("Starting server...")
    logging.info("/docs (GET) (http://%s:%s/docs)", host, port)
    logging.info("/redoc (GET) (http://%s:%s/redoc)", host, port)
    logging.info("/openapi.json (GET) (http://%s:%s/openapi.json)", host, port)
    run(
        app, host=host, port=port, log_level=os.environ.get("LOG_LEVEL", "info").lower()
    )


cli.add_command(run_server)


if __name__ == "__main__":
    try:
        cli()
    except EnvVarNotSetError as e:
        logging.error(str(e))
        sys.exit(1)
