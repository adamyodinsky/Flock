"""Flock Observer Main Module, this module contains the CLI commands for the Flock Observer service."""

import logging
import os
import sys

import click
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flock_common import EnvVarNotSetError, check_env_vars, init_logging
from uvicorn import run

from flock_observer.api import get_router
from flock_observer.observer import ObserverFactory

init_logging(
    destination=os.environ.get("LOG_DESTINATION", "stdout"),
    level=os.environ.get("LOG_LEVEL", "INFO"),
)


@click.group()
def cli():
    """Flock Observer CLI"""


@cli.command(
    help="Run the observer as a server.",
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
def run_observer(host, port):
    """Run the observer as a server."""

    logging.info("Initializing Observer...")

    required_vars = []
    optional_vars = [
        "HOST",
        "PORT",
        "OBSERVER_TYPE",
        "DEFAULT_LABEL_SELECTOR",
    ]

    load_dotenv(find_dotenv(os.environ.get("ENV_FILE", ".env")))
    check_env_vars(required_vars, optional_vars)

    observer = ObserverFactory().get_observer(
        observer_type=os.environ.get("OBSERVER_TYPE", "k8s"),
        default_label_selector=os.environ.get("DEFAULT_LABEL_SELECTOR", "flock=true"),
    )

    api_prefix = os.environ.get("API_PREFIX", "observer")
    app = FastAPI(
        title="Flock Observer",
        description="Flock Observer API",
        version="0.0.1",
        docs_url=f"/{api_prefix}/docs",
        redoc_url=f"/{api_prefix}/redoc",
        openapi_url=f"/{api_prefix}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Allow any origin
        allow_credentials=True,
        allow_methods=["*"],  # Allow any method
        allow_headers=["*"],  # Allow any header
    )

    router = get_router(observer, api_prefix)
    app.include_router(router)

    # Spin up the API server
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
