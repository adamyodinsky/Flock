import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_common import check_env_vars, init_logging
from flock_common.queue_client import QueueClient, QueueClientFactory
from uvicorn import run

from flock_ticket_ingester.routes import create_routes
from flock_ticket_ingester.trello_client import FlockTrelloClient

init_logging()

required_vars = [
    "TRELLO_BOARD_NAME",
    "TRELLO_API_KEY",
    "TRELLO_API_SECRET",
    "TRELLO_TOKEN",
]
optional_vars = [
    "FLOCK_QUEUE_CLIENT",
    "LOG_LEVEL",
    "LOG_FILE",
    "QUEUE_NAME",
    "QUEUE_HOST",
    "QUEUE_PORT",
    "QUEUE_VHOST",
    "QUEUE_USERNAME",
    "QUEUE_PASSWORD",
    "HOST",
    "PORT",
]

load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
check_env_vars(required_vars, optional_vars)
queue_client = QueueClientFactory.get_client(
    os.environ.get("FLOCK_QUEUE_CLIENT", "rabbitmq"),
    queue_name=os.environ.get("QUEUE_NAME", "todo_tickets"),
    host=os.environ.get("QUEUE_HOST", "localhost"),
    port=int(os.environ.get("QUEUE_PORT", 5672)),
    vhost=os.environ.get("QUEUE_VHOST", "/"),
    username=os.environ.get("QUEUE_USERNAME", "root"),
    password=os.environ.get("QUEUE_PASSWORD", "password"),
)


queue_client.connect()

flock_trello = FlockTrelloClient(
    board_name=os.environ.get("TRELLO_BOARD_NAME"),
    api_key=os.environ.get("TRELLO_API_KEY"),
    api_secret=os.environ.get("TRELLO_API_SECRET"),
    token=os.environ.get("TRELLO_TOKEN"),
)
todo_list_id = flock_trello.get_list_id("todo")

app = FastAPI()
routes = create_routes(
    queue_client=queue_client, trello_client=flock_trello, todo_list_id=todo_list_id
)

app.include_router(routes)

host = os.environ.get("HOST", "localhost")
port = int(os.environ.get("PORT", 9000))

run(app, host=host, port=port, log_level=os.environ.get("LOG_LEVEL", "info"))
