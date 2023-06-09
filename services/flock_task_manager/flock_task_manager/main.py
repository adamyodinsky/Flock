import logging

from flock_common.logging import init_logging

init_logging()

import os
from threading import Thread

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from uvicorn import run

from flock_common import check_env_vars
from flock_common.queue_client import QueueClient, QueueClientFactory
from flock_task_management_store import TaskManagementStoreFactory
from flock_task_manager.routes import create_routes
from flock_task_manager.task_manager import TaskManager

required_vars = []
optional_vars = [
    "QUEUE_CLIENT",
    "QUEUE_NAME",
    "QUEUE_HOST",
    "QUEUE_PORT",
    "QUEUE_VHOST",
    "QUEUE_USERNAME",
    "QUEUE_PASSWORD",
    "MANAGEMENT_STORE_DB_NAME",
    "MANAGEMENT_STORE_COLLECTION_NAME",
    "MANAGEMENT_STORE_USERNAME",
    "MANAGEMENT_STORE_PASSWORD",
    "MANAGEMENT_STORE_HOST",
    "HOST",
    "PORT",
    "LOG_LEVEL",
]
load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
check_env_vars(required_vars, optional_vars)


queue_client = QueueClientFactory.get_client(
    os.environ.get("QUEUE_CLIENT", "rabbitmq"),
    queue_name=os.environ.get("QUEUE_NAME", "todo_tickets"),
    host=os.environ.get("QUEUE_HOST", "localhost"),
    port=int(os.environ.get("QUEUE_PORT", 5672)),
    vhost=os.environ.get("QUEUE_VHOST", "/"),
    username=os.environ.get("QUEUE_USERNAME", "root"),
    password=os.environ.get("QUEUE_PASSWORD", "password"),
)

queue_client.connect()


def run_task_manager(queue_client: QueueClient):
    task_mgmt_store = TaskManagementStoreFactory.get_store(
        os.environ.get("FLOCK_MANAGEMENT_STORE_TYPE", "mongo"),
        db_name=os.environ.get("MANAGEMENT_STORE_DB_NAME", "flock_db"),
        collection_name=os.environ.get("MANAGEMENT_STORE_COLLECTION_NAME", "tickets"),
        host=os.environ.get("MANAGEMENT_STORE_HOST", "localhost"),
        port=int(os.environ.get("MANAGEMENT_STORE_PORT", 27017)),
        username=os.environ.get("MANAGEMENT_STORE_USERNAME", "root"),
        password=os.environ.get("MANAGEMENT_STORE_PASSWORD", "password"),
    )

    task_manager = TaskManager(queue_client=queue_client, db_client=task_mgmt_store)

    task_manager.manage_tasks()


def run_server(queue_client):
    routes = create_routes(queue_client)
    server = FastAPI()
    server.include_router(routes)

    host = os.environ.get("HOST", "localhost")
    port = int(os.environ.get("PORT", 7000))
    run(server, host=host, port=port, log_level=os.environ.get("LOG_LEVEL", "info"))


queue_thread = Thread(target=run_task_manager, args=(queue_client,))
server_thread = Thread(target=run_server, args=(queue_client,))

queue_thread.start()
server_thread.start()

queue_thread.join()
server_thread.join()
