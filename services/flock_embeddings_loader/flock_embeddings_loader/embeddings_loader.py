"""Embeddings Loader class"""

import logging
from typing import cast

import click
from flock_builder.resource_builder import ResourceBuilder
from pydantic import ValidationError
from resources.embeddings_loader import EmbeddingsLoaderResource
from flock_resource_store import ResourceStoreFactory


class FlockEmbeddingsLoader:
    """Flock Embeddings class"""

    def __init__(self, manifest: dict):
        """Initialize the Embeddings Loader"""

        try:
            self.resource_store = ResourceStoreFactory.get_resource_store()
            self.manifest = manifest
            self.builder = ResourceBuilder(resource_store=self.resource_store)
            self.embeddings_loader: EmbeddingsLoaderResource = cast(
                EmbeddingsLoaderResource,
                self.builder.build_resource(manifest=self.manifest),
            )
        except ValidationError as error:
            logging.error("Invalid configuration manifest %s", str(error))
            raise click.ClickException(
                f"Invalid configuration manifest: {str(error)}"
            ) from error
        except Exception as error:
            logging.error(
                "Error while initializing embeddings loader job %s", str(error)
            )
            raise click.ClickException(
                f"Error while initializing embeddings loader job: {str(error)}"
            ) from error

    def start_scraped__data_job(self):
        """Start the embeddings loader job"""

        try:
            logging.info("Loading scraped data to vectorstore...")
            self.embeddings_loader.load_scraped_data_to_vectorstore()
        except Exception as error:  # pylint: disable=broad-except
            logging.error("Error while loading scraped data to vectorstore %s", error)
            raise click.ClickException(
                f"Error while loading scraped data to vectorstore: {error}"
            ) from error

    def start_raw_files_job(self):
        """Start the embeddings loader job"""

        try:
            logging.info("Loading raw files to vectorstore...")
            self.embeddings_loader.load_files_to_vectorstore()
        except Exception as error:  # pylint: disable=broad-except
            logging.error("Error while loading raw files to vectorstore %s", error)
            raise click.ClickException(
                f"Error while loading raw files to vectorstore: {error}"
            ) from error
