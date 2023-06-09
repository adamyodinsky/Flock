"""Main module for the Flock Embeddings Loader CLI"""

import json
import os
import sys

import click
from dotenv import find_dotenv, load_dotenv
from flock_common import EnvVarNotSetError, check_env_vars

from flock_embeddings_loader.embeddings_loader import FlockEmbeddingsLoader


@click.group()
def cli():
    """Flock Embeddings Loader CLI"""


@cli.command(
    help="Run embeddings loader job.",
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
# scraped data or raw files
@click.option(
    "--loader-type",
    help="Type of job to run.",
    default=os.environ.get("FLOCK_LOADER_TYPE", None),
    type=click.Choice(["scraped-data", "raw-files"]),
)
def run_job(schema_path, schema_value, loader_type):
    """Run embeddings loader job."""

    config_str = ""
    click.echo("Initializing...")

    # Check env vars
    required_vars = []
    optional_vars = [
        "FLOCK_SCHEMA_PATH",
        "FLOCK_SCHEMA_VALUE",
        "FLOCK_LOADER_TYPE",
        "ALLOWED_EXTENSIONS",
        "DENY_EXTENSIONS",
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
            print(f"Error: File {schema_path} not found.")
            sys.exit(1)
    elif schema_value:
        config_str = json.loads(schema_value)
    else:
        raise click.UsageError("Either --schema-path or --schema-value is required.")

    # Initialize object with the configuration manifest
    flock_embeddings_loader = FlockEmbeddingsLoader(config_str)

    # Run the embeddings loader job
    click.echo("Ready. Running job...")

    if loader_type == "scraped-data":
        # Run the embeddings loader job
        click.echo("Ready. Running job...")
        flock_embeddings_loader.start_scraped__data_job()
    elif loader_type == "raw-files":
        # Run the embeddings loader job
        click.echo("Ready. Running job...")
        flock_embeddings_loader.start_raw_files_job()
    else:
        raise click.UsageError("Either --loader-type is required.")


cli.add_command(run_job)

if __name__ == "__main__":
    try:
        cli()
    except EnvVarNotSetError as e:
        print(str(e))
        sys.exit(1)
