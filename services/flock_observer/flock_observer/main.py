import logging
import os
import sys

import click
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_common import EnvVarNotSetError, check_env_vars
from flock_common.logging import init_logging
from uvicorn import run

from flock_observer.api import get_router
from flock_observer.observer import ObserverFactory

init_logging(
    destination=os.environ.get("FLOCK_LOG_DESTINATION", "stdout"),
)


@click.group()
def cli():
    """Flock Agent CLI"""


@cli.command(
    help="Run the observer as a server.",
)
@click.option(
    "--host",
    default=os.environ.get("FLOCK_AGENT_HOST", "127.0.0.1"),
    help="The host address to bind the server to.",
)
@click.option(
    "--port",
    default=os.environ.get("FLOCK_AGENT_PORT", 8080),
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
        "LOG_FILE",
        "LOG_LEVEL",
        "OBSERVER_TYPE",
        "DEFAULT_LABEL_SELECTOR",
    ]

    load_dotenv(find_dotenv(os.environ.get("ENV_FILE", ".env")))
    check_env_vars(required_vars, optional_vars)

    # Create the observer
    observer = ObserverFactory().get_observer(
        observer_type=os.environ.get("OBSERVER_TYPE", "k8s"),
        default_label_selector=os.environ.get("DEFAULT_LABEL_SELECTOR", "flock=true"),
    )

    app = FastAPI(
        title="Flock Observer",
        description="Flock Observer API",
        version="0.0.1",
    )
    router = get_router(observer)
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
