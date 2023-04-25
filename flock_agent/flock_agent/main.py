import json
import os
import sys

import click
from fastapi import FastAPI
from uvicorn import run

from flock_agent.agent import FlockAgent
from flock_agent.routes import create_agent_routes


@click.group()
def cli():
    """Flock Agent CLI"""


@cli.command(
    help="Run the agent as a server. The agent will listen for requests on /agent."
)
@click.option(
    "--input-path",
    help="Path to the configuration manifest file.",
    default=os.environ.get("INPUT_PATH", None),
)
@click.option(
    "--input-value",
    help="Configuration manifest as a JSON string.",
    default=os.environ.get("INPUT_VALUE", None),
)
@click.option(
    "--host",
    default=os.environ.get("HOST", "127.0.0.1"),
    help="The host address to bind the server to.",
)
@click.option(
    "--port",
    default=os.environ.get("PORT", 8000),
    type=int,
    help="The port the server should listen on.",
)
def run_agent(input_path, input_value, host, port):
    """Run the agent as a server."""

    config_str = ""
    click.echo("Initializing...")

    # Load configuration manifest from a file or a string
    if input_path:
        if os.path.exists(input_path):
            with open(input_path, "r", encoding="utf-8") as f:
                config_str = f.read()
                config_str = json.loads(config_str)
        else:
            print(f"Error: File {input_path} not found.")
            sys.exit(1)
    elif input_value:
        config_str = json.loads(input_value)
    else:
        raise click.UsageError("Either --input-path or --input-value must be provided.")

    # Initialize agent object with the configuration manifest
    flock_agent = FlockAgent(config_str)

    # Create FastAPI app and include the agent routes
    app = FastAPI()
    routes = create_agent_routes(flock_agent)
    app.include_router(routes)

    # Spin up the API server
    click.echo(f"Ready. Waiting for requests on {host}:{port}...")
    click.echo("/agent (POST) (http://localhost:8000/agent")
    click.echo("/agent_ws (WebSocket) (ws://localhost:8000/agent_ws)")

    run(app, host=host, port=port, log_level="warning")


cli.add_command(run_agent)

if __name__ == "__main__":
    cli()
