import json
import logging
import os
import sys

import click
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_agent.agent import FlockAgent
from flock_agent.routes import create_agent_routes
from flock_common import EnvVarNotSetError, check_env_vars
from flock_common.logging import init_logging
from flock_common.queue_client import QueueClientFactory
from flock_resource_store import ResourceStoreFactory
from flock_task_management_store import TaskManagementStoreFactory
from uvicorn import run

init_logging(
    destination=os.environ.get("FLOCK_LOG_DESTINATION", "stdout"),
)


@click.group()
def cli():
    """Flock Agent CLI"""


@cli.command(
    help="Run the agent as a server. The agent will listen for requests on /agent."
)
@click.option(
    "--schema-path",
    help="Path to the configuration manifest file.",
    default=os.environ.get("FLOCK_SCHEMA_PATH", None),
)
@click.option(
    "--schema-value",
    help="Configuration manifest as a JSON string.",
    default=os.environ.get("FLOCK_SCHEMA_VALUE", None),
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
def run_agent(schema_path, schema_value, host, port):
    """Run the agent as a server."""

    config_str = ""
    logging.info("Initializing Flock Agent...")

    # Check env vars
    required_vars = []
    optional_vars = [
        "FLOCK_SCHEMA_PATH",
        "FLOCK_SCHEMA_VALUE",
        "FLOCK_AGENT_HOST",
        "FLOCK_AGENT_PORT",
        "FLOCK_MANAGEMENT_STORE_TYPE",
        "MANAGEMENT_STORE_DB_NAME",
        "MANAGEMENT_STORE_TICKET_TABLE_NAME",
        "MANAGEMENT_STORE_HOST",
        "MANAGEMENT_STORE_PORT",
        "MANAGEMENT_STORE_USERNAME",
        "MANAGEMENT_STORE_PASSWORD",
        "FLOCK_RESOURCE_STORE_TYPE",
        "RESOURCE_STORE_DB_NAME",
        "RESOURCE_STORE_TABLE_NAME",
        "RESOURCE_STORE_HOST",
        "RESOURCE_STORE_PORT",
        "RESOURCE_STORE_USERNAME",
        "RESOURCE_STORE_PASSWORD",
        "QUEUE_CLIENT",
        "QUEUE_NAME",
        "QUEUE_HOST",
        "QUEUE_PORT",
        "QUEUE_VHOST",
        "QUEUE_USERNAME",
        "QUEUE_PASSWORD",
        "FLOCK_AGENT_HOST",
        "FLOCK_AGENT_PORT",
        "LOG_FILE",
        "LOG_LEVEL",
    ]
    load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
    check_env_vars(required_vars, optional_vars)

    # Load configuration manifest from a file or a string
    if schema_path:
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                config_str = f.read()
                config_str = json.loads(config_str)
        else:
            logging.fatal("File %s does not exist.", schema_path)
            sys.exit(1)
    elif schema_value:
        config_str = json.loads(schema_value)
    else:
        logging.fatal("Either --schema-path or --schema-value is required.")
        raise click.UsageError("Either --schema-path or --schema-value is required.")

    task_management_store = TaskManagementStoreFactory.get_store(
        store_type=os.environ.get("FLOCK_MANAGEMENT_STORE_TYPE", "mongo"),
        db_name=os.environ.get("MANAGEMENT_STORE_DB_NAME", "flock_db"),
        tickets_table_name=os.environ.get(
            "MANAGEMENT_STORE_TICKET_TABLE_NAME", "tickets"
        ),
        locks_table_name=os.environ.get(
            "MANAGEMENT_STORE_LOCKS_TABLE_NAME", "tickets_locks"
        ),
        host=os.environ.get("MANAGEMENT_STORE_HOST", "localhost"),
        port=int(os.environ.get("MANAGEMENT_STORE_PORT", 27017)),
        username=os.environ.get("MANAGEMENT_STORE_USERNAME", "root"),
        password=os.environ.get("MANAGEMENT_STORE_PASSWORD", "password"),
    )

    resource_store = ResourceStoreFactory.get_resource_store(
        store_type=os.environ.get("FLOCK_RESOURCE_STORE_TYPE", "mongo"),
        db_name=os.environ.get("RESOURCE_STORE_DB_NAME", "flock_db"),
        table_name=os.environ.get("RESOURCE_STORE_TABLE_NAME", "flock_resources"),
        host=os.environ.get("RESOURCE_STORE_HOST", "localhost"),
        port=int(os.environ.get("RESOURCE_STORE_PORT", 27017)),
        username=os.environ.get("RESOURCE_STORE_USERNAME", "root"),
        password=os.environ.get("RESOURCE_STORE_PASSWORD", "password"),
    )

    queue_client = QueueClientFactory.get_client(
        os.environ.get("QUEUE_CLIENT", "rabbitmq"),
        queue_name=os.environ.get("QUEUE_NAME", "todo_tickets"),
        host=os.environ.get("QUEUE_HOST", "localhost"),
        port=int(os.environ.get("QUEUE_PORT", 5672)),
        vhost=os.environ.get("QUEUE_VHOST", "/"),
        username=os.environ.get("QUEUE_USERNAME", "root"),
        password=os.environ.get("QUEUE_PASSWORD", "password"),
    )

    # Initialize agent object with the configuration manifest
    flock_agent = FlockAgent(
        manifest=config_str,
        resource_store=resource_store,
        queue_client=queue_client,
        task_mgmt_store=task_management_store,
    )

    # Create FastAPI app and include the agent routes
    app = FastAPI(
        title="Flock Agent",
        description="A Flock Agent is a server that can be used to run Flock tasks.",
        version="0.0.1",
    )
    router = create_agent_routes(flock_agent)
    app.include_router(router)

    host = os.environ.get("FLOCK_AGENT_HOST", host)
    port = int(os.environ.get("FLOCK_AGENT_PORT", port))

    # Spin up the API server
    logging.info("Starting Flock Agent on %s:%s", host, port)
    logging.info("/docs (GET) (http://%s:%s/docs)", host, port)
    logging.info("/redoc (GET) (http://%s:%s/redoc)", host, port)
    logging.info("/openapi.json (GET) (http://%s:%s/openapi.json)", host, port)
    for route in router.routes:
        logging.info("%s (%s)", route.path, route.methods)  # type: ignore
    run(app, host=host, port=port, log_level=os.environ.get("LOG_LEVEL", "info"))


cli.add_command(run_agent)

if __name__ == "__main__":
    try:
        cli()
    except EnvVarNotSetError as e:
        logging.error(str(e))
        sys.exit(1)
