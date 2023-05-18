"""Flock Agent class"""
import os
from typing import cast

import click
from flock_models.builder.resource_builder import ResourceBuilder
from flock_models.resources.base import Agent
from flock_resource_store import ResourceStoreFactory
from pydantic import ValidationError


class FlockAgent:
    """Flock Agent class"""

    def __init__(self, manifest: dict):
        """Initialize Flock Agent"""

        self.config = {
            "leader_addr": os.environ.get("MAINFRAME_ADDR", "http://localhost:5000"),
        }

        try:
            self.resource_store = ResourceStoreFactory.get_resource_store()
            self.manifest = manifest
            self.builder = ResourceBuilder(resource_store=self.resource_store)
            self.agent: Agent = cast(
                Agent, self.builder.build_resource(manifest=self.manifest)
            )
        except ValidationError as error:
            raise click.ClickException(
                f"Invalid configuration manifest: {str(error)}"
            ) from error
        except Exception as error:
            raise click.ClickException(
                f"Error while initializing agent: {str(error)}"
            ) from error

    def get_response(self, message):
        """Get response from the agent"""

        response: str = ""

        try:
            response = self.agent.run(message)  # type: ignore
        except Exception as error:  # pylint: disable=broad-except
            response = f"Sorry, i'm experiencing an error. {str(error)}"
            print(f"Error: {error}")

        return response
