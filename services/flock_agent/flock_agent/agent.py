"""Flock Agent class"""
import logging
import os
import queue
import threading
from typing import cast

import click
from flock_builder.resource_builder import ResourceBuilder
from flock_common.queue_client import QueueClient
from flock_resource_store import ResourceStore
from flock_resources.base import Agent
from flock_task_management_store.mongo import (
    MongoTaskManagementStore,
    TaskManagementStore,
)
from pydantic import ValidationError

MINUTE = 60
HOUR = 60 * MINUTE


class FlockAgent:
    """Flock Agent class"""

    def __init__(
        self,
        manifest: dict,
        resource_store: ResourceStore,
        queue_client: QueueClient,
        task_mgmt_store: TaskManagementStore,
    ):
        """Initialize Flock Agent"""

        self.config = {
            "leader_addr": os.environ.get("MAINFRAME_ADDR", "http://localhost:5000"),
        }

        self.queue_client = queue_client
        self.task_mgmt_store = task_mgmt_store
        self.thread_mail_box = queue.Queue()

        try:
            self.resource_store = resource_store
            self.manifest = manifest
            self.builder = ResourceBuilder(resource_store=self.resource_store)
            self.agent = cast(
                Agent, self.builder.build_resource(manifest=self.manifest)
            )
        except ValidationError as error:
            logging.error(f"Invalid configuration manifest: {str(error)}")
            raise click.ClickException(
                f"Invalid configuration manifest: {str(error)}"
            ) from error
        except Exception as error:
            logging.error(f"Error while initializing agent: {error}")
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
            logging.error(f"Error while running agent: {str(error)}")

        return response

    def _acquire_and_handle(self, ticket):
        if self.task_mgmt_store.acquire_lock(ticket):
            self.task_mgmt_store.tickets_table.update_one(
                {"_id": ticket["id"]}, {"$set": {"idList": "in_progress"}}
            )
            result = self.agent.run(ticket)  # type: ignore
            self.queue_client.produce(result)

    def handle_tasks_loop(self):
        """Handle tasks loop

        This function is responsible for handling tasks from the task management store.
        """

        while True:
            ticket = self.task_mgmt_store.query({"idList": "todo"})
            if ticket:
                self._acquire_and_handle(ticket)
            else:
                thread = threading.Thread(
                    target=self.task_mgmt_store.watch_on_insert,
                    args=(self.thread_mail_box,),
                )
                thread.start()
                thread.join(timeout=5 * MINUTE)  # timeout for watch on insert

                if not self.thread_mail_box.empty():
                    ticket = self.thread_mail_box.get()
                if ticket:
                    self._acquire_and_handle(ticket)
            ticket = None
