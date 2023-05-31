"""Trello CLI."""
import os
from typing import Dict, Optional

import click
from dotenv import find_dotenv, load_dotenv
from flock_common import check_env_vars
from pydantic import BaseModel
from trello import TrelloClient, exceptions


class HttpResponse(BaseModel):
    """Trello webhook data."""

    status_code: int


class FlockTrelloClient:
    """Flock Trello client."""

    def __init__(self):
        """Initialize the Flock Trello client."""
        # Check env vars
        required_vars = [
            "TRELLO_API_KEY",
            "TRELLO_API_SECRET",
            "TRELLO_TOKEN",
            "TRELLO_BOARD_NAME",
        ]
        optional_vars = []
        load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
        check_env_vars(required_vars, optional_vars)

        self.client = TrelloClient(
            api_key=os.environ.get("TRELLO_API_KEY"),
            api_secret=os.environ.get("TRELLO_API_SECRET"),
            token=os.environ.get("TRELLO_TOKEN"),
        )
        self.board_name = os.environ.get("TRELLO_BOARD_NAME")
        self.board_id = self.get_board_id()

        try:
            self.client.list_boards()
        except Exception as error:
            raise exceptions.ResourceUnavailable(
                "Failed to create Trello client", 500
            ) from error

    def get_board_id(self, board_name=None):
        """Get the board id from a board name."""

        if board_name is None:
            board_name = self.board_name

        for board in self.client.list_boards():
            if board.name == self.board_name:
                return board.id
        raise exceptions.ResourceUnavailable(
            f"No board found with the name {self.board_name}", 404
        )

    def create_trello_webhook(self, callback_url, board_id=None):
        """Create a webhook for the Trello board."""

        if board_id is None:
            board_id = self.board_id

        hook = self.client.create_hook(
            callback_url=callback_url,
            id_model=self.board_id,
        )

        if hook is None:
            # raise specific exception
            raise exceptions.ResourceUnavailable("Failed to create webhook", 500)

        click.echo("Webhook created successfully")
        click.echo(f"Webhook ID: {hook.id}")

    def delete_trello_webhook(self, callback_url, board_id=None):
        """Delete a webhook for the Trello board."""
        if board_id is None:
            board_id = self.board_id

        hooks = self.client.list_hooks()
        # search and delete the webhook
        for hook in hooks:
            if hook.callback_url == callback_url and hook.id_model == self.board_id:
                hook.delete()
                click.echo("Webhook deleted successfully")
                return

        # raise Exception("Failed to delete webhook, not found")
        raise exceptions.ResourceUnavailable(
            "Failed to delete webhook, not found", HttpResponse(status_code=404)
        )

    def get_list_id(self, list_name, board_id=None):
        """Get the list id from a list name."""

        if board_id is None:
            board_id = self.board_id

        board = self.client.get_board(board_id)
        lists = board.list_lists()

        for list_ in lists:
            if list_.name.lower() == list_name.lower():
                print(f"List ID: {list_.id}, List Name: {list_.name}")
                return list_.id

        raise exceptions.ResourceUnavailable(
            f"No list found with the name {list_name}", 404
        )

    class TrelloData(BaseModel):
        """Trello webhook data."""

        action: Dict
        model: Optional[Dict] = None


@click.group()
@click.pass_context
def cli(ctx):
    """Trello CLI."""

    ctx.ensure_object(dict)
    trello_client = FlockTrelloClient()
    ctx.obj["trello_client"] = trello_client


@click.command()
@click.option(
    "--board-name",
    required=True,
    help="The name of the Trello board to create a webhook for.",
    default=os.environ.get("TRELLO_BOARD_NAME"),
)
@click.option(
    "--callback-url",
    required=True,
    help="The URL to call when the webhook is triggered.",
    default=os.environ.get("CALLBACK_URL"),
)
@click.pass_context
def create_trello_webhook(ctx, board_name, callback_url):
    """Create a webhook for the Trello board."""

    trello_client: FlockTrelloClient = ctx.obj["trello_client"]
    trello_client.create_trello_webhook(board_name, callback_url)


@click.command()
@click.option(
    "--callback-url",
    required=True,
    help="The URL to call when the webhook is triggered.",
    default=os.environ.get("CALLBACK_URL"),
)
@click.option(
    "--board-name",
    required=True,
    help="The name of the Trello board to create a webhook for.",
    default=os.environ.get("TRELLO_BOARD_NAME"),
)
def delete_trello_webhook(callback_url, board_name):
    """Delete a webhook for the Trello board."""

    trello_client: FlockTrelloClient = FlockTrelloClient()
    trello_client.delete_trello_webhook(board_name, callback_url)


# get list id command
@click.command()
@click.option(
    "--list-name",
    required=True,
    help="The name of the Trello list to get the ID for.",
    default=os.environ.get("TRELLO_LIST_NAME"),
)
@click.pass_context
def get_list_id(ctx, list_name):
    """Get the list id from a list name."""

    trello_client: FlockTrelloClient = ctx.obj["trello_client"]
    trello_client.get_list_id(list_name)


cli.add_command(create_trello_webhook)
cli.add_command(delete_trello_webhook)
cli.add_command(get_list_id)

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
