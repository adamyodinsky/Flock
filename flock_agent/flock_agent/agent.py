"""Flock Agent class"""
import os
import threading
from typing import cast

import click
from flock_common.queue_client import QueueClient
from flock_models.builder.resource_builder import ResourceBuilder
from flock_models.resources.base import Agent
from flock_resource_store import ResourceStore
from flock_task_management_store.mongo import (
    MongoTaskManagementStore,
    TaskManagementStore,
)
from pydantic import ValidationError


class FlockAgent:
    """Flock Agent class"""

    def __init__(
        self,
        manifest: dict,
        resource_store: ResourceStore,
        queue_client: QueueClient,
        task_mgmt_store: MongoTaskManagementStore,
    ):
        """Initialize Flock Agent"""

        self.config = {
            "leader_addr": os.environ.get("MAINFRAME_ADDR", "http://localhost:5000"),
        }

        self.queue_client = queue_client
        self.task_mgmt_store = task_mgmt_store
        try:
            self.resource_store = resource_store
            self.manifest = manifest
            self.builder = ResourceBuilder(resource_store=self.resource_store)
            self.agent = cast(
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
            response = f"Sorry, i'm experiencing an error.\n\nError:{str(error)}"
            print(f"Error: {error}")

        return response

    def handle_task(self):
        """
        Handle the task

        """

        while True:
            ticket = self.task_mgmt_store.query({"idList": "todo"})
            if ticket:
                if self.task_mgmt_store.acquire_lock(ticket):
                    self.task_mgmt_store.tickets_table.update_one(
                        {"_id": ticket["id"]}, {"$set": {"idList": "in_progress"}}
                    )
                    result = self.agent.run(ticket)  # type: ignore
                    self.queue_client.produce(result)
            else:
                thread = threading.Thread(
                    target=self.task_mgmt_store.watch_insert_stream
                )
                thread.start()
                thread.join(timeout=60 * 60)
                if ticket:
                    if self.task_mgmt_store.acquire_lock(ticket):
                        result = self.agent.run(ticket)  # type: ignore
                        self.queue_client.produce(result)
