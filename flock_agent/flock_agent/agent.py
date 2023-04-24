import os

import click
from flock_models.builder.resource_builder import ResourceBuilder
from flock_schemas.custom import CustomSchema
from flock_resource_store import ResourceStoreFactory
from pydantic import ValidationError


class FlockAgent:
    def __init__(self, manifest: CustomSchema):
        home_dir = os.path.expanduser("~")

        self.config = {
            "key_prefix": os.environ.get(
                "RESOURCE_STORE_KEY_PREFIX", f"{home_dir}/.flock/resource_store"
            ),
            "store_type": os.environ.get("RESOURCE_STORE_TYPE", "fs"),
            "leader_addr": os.environ.get("MAINFRAME_ADDR", "http://localhost:5000"),
        }
        
        try:
            self.resource_store = ResourceStoreFactory.get_resource_store(
                store_type=self.config["store_type"],
                key_prefix=self.config["key_prefix"],
            )
            self.manifest = CustomSchema(**manifest)
            self.builder = ResourceBuilder(
                resource_store=self.resource_store, secret_store=None
            )
            self.agent = self.builder.build_resource(manifest=self.manifest)
        except ValidationError as error:
            raise click.ClickException(f"Invalid configuration manifest: {str(error)}")
        except Exception as error:
            raise click.ClickException(f"Error while initializing agent: {str(error)}")

    def get_response(self, message):
        response: str = ""

        try:
            response = self.agent.run(message)
        except Exception as error:
            response = f"Error: {str(error)}"

        return response
