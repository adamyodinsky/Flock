"""Main module for the Flock Embeddings Loader CLI"""

import json
import logging
import os
import sys

import click
from dotenv import find_dotenv, load_dotenv
from flock_common import EnvVarNotSetError, check_env_vars
from flock_common.logging import init_logging
from flock_embeddings_loader.embeddings_loader import FlockEmbeddingsLoader
from flock_resource_store import ResourceStoreFactory

init_logging(
    destination=os.environ.get("LOG_DESTINATION", "stdout"),
)


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
@click.option(
    "--loader-type",
    help="Type of job to run.",
    default=os.environ.get("FLOCK_LOADER_TYPE", None),
    type=click.Choice(["scraped-data", "raw-files"]),
)
def run_job(schema_path, schema_value, loader_type):
    """Run embeddings loader job."""

    config_str = ""
    logging.info("Starting Flock Embeddings Loader...")

    # Check env vars
    required_vars = []
    optional_vars = [
        "FLOCK_SCHEMA_PATH",
        "FLOCK_SCHEMA_VALUE",
        "FLOCK_LOADER_TYPE",
        "ALLOWED_EXTENSIONS",
        "DENY_EXTENSIONS",
        "FLOCK_RESOURCE_STORE_TYPE",
        "RESOURCE_STORE_DB_NAME",
        "RESOURCE_STORE_TABLE_NAME",
        "RESOURCE_STORE_HOST",
        "RESOURCE_STORE_PORT",
        "RESOURCE_STORE_USERNAME",
        "RESOURCE_STORE_PASSWORD",
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
            logging.fatal("Error: Schema file not found.")
            sys.exit(1)
    elif schema_value:
        config_str = json.loads(schema_value)
    else:
        raise click.UsageError("Either --schema-path or --schema-value is required.")

    resource_store = ResourceStoreFactory.get_resource_store(
        store_type=os.environ.get("FLOCK_RESOURCE_STORE_TYPE", "mongo"),
        db_name=os.environ.get("RESOURCE_STORE_DB_NAME", "flock_db"),
        table_name=os.environ.get("RESOURCE_STORE_TABLE_NAME", "flock_resources"),
        host=os.environ.get("RESOURCE_STORE_HOST", "localhost"),
        port=int(os.environ.get("RESOURCE_STORE_PORT", 27017)),
        username=os.environ.get("RESOURCE_STORE_USERNAME", "root"),
        password=os.environ.get("RESOURCE_STORE_PASSWORD", "password"),
    )

    flock_embeddings_loader = FlockEmbeddingsLoader(config_str, resource_store)

    logging.info("Ready. Running job...")

    if loader_type == "scraped-data":
        logging.info("Loading scraped data to vectorstore...")
        flock_embeddings_loader.start_scraped_data_job()
    elif loader_type == "raw-files":
        logging.info("Loading raw files to vectorstore...")
        flock_embeddings_loader.start_raw_files_job()
    else:
        logging.error("Error: Invalid loader type.")
        raise click.UsageError("Either --loader-type is required.")


cli.add_command(run_job)

if __name__ == "__main__":
    try:
        cli()
    except EnvVarNotSetError as e:
        print(str(e))
        sys.exit(1)
