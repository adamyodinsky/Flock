from fastapi import APIRouter, Depends, FastAPI, Response
from flock_common.queue_client import QueueClient
from trello import Card

from flock_ticket_ingester.trello_client import FlockTrelloClient

app = FastAPI()
router = APIRouter()


def is_todo_queue_eligible(card: Card, todo_list_id) -> bool:
    """Check if a card is eligible for sending to the todo queue."""
    card_labels = [label.name for label in card.labels]

    result = (
        "ai_enabled" in card_labels and not card.closed and card.list_id == todo_list_id
    )

    return result


def create_routes(
    queue_client: QueueClient, trello_client: FlockTrelloClient, todo_list_id: str
):
    """Create routes for the agent."""

    @router.get("/")
    async def health_check():
        return Response(status_code=200)

    @router.head("/")
    async def head():
        return Response(status_code=200)

    @router.post("/")
    async def webhook(
        req: FlockTrelloClient.TrelloData,
        queue_client: QueueClient = Depends(lambda: queue_client),
        flock_trello: FlockTrelloClient = Depends(lambda: trello_client),
    ):
        """Handle Trello webhook data."""

        card = req.action.get("data", {}).get("card", None)
        if card:
            full_card: Card = flock_trello.client.get_card(card.get("id", None))

            if is_todo_queue_eligible(full_card, todo_list_id):
                queue_client.send(full_card._json_obj)
                print(f"Sent card {full_card.id} to queue")

        return Response(status_code=200)

    return router
