import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from flock_common import check_env_vars
from flock_common.queue_client import QueueClientFactory
from uvicorn import run

from flock_ticket_ingester.routes import create_routes
from flock_ticket_ingester.trello_client import FlockTrelloClient

host = os.environ.get("HOST", "localhost")
port = int(os.environ.get("PORT", 9000))

required_vars = []
optional_vars = ["FLOCK_QUEUE_CLIENT"]
load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
check_env_vars(required_vars, optional_vars)

queue_client_cls = QueueClientFactory.get_queue_client(
    os.environ.get("FLOCK_QUEUE_CLIENT", "rabbitmq")
)

queue_client = queue_client_cls()
queue_client.connect()

flock_trello = FlockTrelloClient()
todo_list_id = flock_trello.get_list_id("todo")

app = FastAPI()
routes = create_routes(
    queue_client=queue_client, trello_client=flock_trello, todo_list_id=todo_list_id
)
app.include_router(routes)

run(app, host=host, port=port, log_level=os.environ.get("LOG_LEVEL", "info"))
