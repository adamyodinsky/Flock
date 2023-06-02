"""Trello CLI."""
import logging
import os
from typing import Dict, Optional

import click
from dotenv import find_dotenv, load_dotenv
from flock_common import check_env_vars, init_logging
from pydantic import BaseModel
from trello import TrelloClient, exceptions


class HttpResponse(BaseModel):
    """Trello webhook data."""

    status_code: int


class FlockTrelloClient:
    """Flock Trello client."""

    def __init__(self, board_name, api_key, api_secret, token):
        """Initialize the Flock Trello client.

        Args:
            board_name (str): The name of the Trello board to create a webhook for.
            api_key (str): The Trello API key.
            api_secret (str): The Trello API secret.
            token (str): The Trello token.

        Raises:
            ValueError: If the board_name, api_key, api_secret, or token are not provided.
        """
        # Check env vars
        required_vars = []
        optional_vars = [
            "TRELLO_API_KEY",
            "TRELLO_API_SECRET",
            "TRELLO_TOKEN",
            "TRELLO_BOARD_NAME",
        ]

        api_key = api_key
        api_secret = api_secret
        token = token
        board_name = board_name

        try:
            self.client = TrelloClient(
                api_key=api_key,
                api_secret=api_secret,
                token=token,
            )
        except Exception as err:
            logging.error("Failed to initialize Trello client: %s", err)
            raise err

        self.board_name = board_name
        self.board_id = self.get_board_id()

        logging.debug("Trello client initialized successfully")

    def get_board_id(self, board_name=None):
        """Get the board id from a board name."""

        if board_name is None:
            board_name = self.board_name

        logging.debug("Getting board ID for board name %s", board_name)

        for board in self.client.list_boards():
            if board.name == self.board_name:
                logging.debug("Board ID: %s", board.id)
                return board.id

        logging.error("No board found with the name %s", self.board_name)
        raise exceptions.ResourceUnavailable(
            f"No board found with the name {self.board_name}",
            404,
        )

    def create_trello_webhook(self, callback_url, board_id=None):
        """Create a webhook for the Trello board."""

        if board_id is None:
            board_id = self.board_id

        logging.debug("Creating webhook for board ID %s", board_id)

        hook = self.client.create_hook(
            callback_url=callback_url,
            id_model=self.board_id,
        )

        if hook is None:
            logging.error(
                "Failed to create webhook for board ID %s callback_url %s",
                board_id,
                callback_url,
            )
            raise exceptions.ResourceUnavailable("Failed to create webhook", 500)

        logging.info("Webhook created successfully with ID %s", hook.id)

    def delete_trello_webhook(self, callback_url, board_id=None):
        """Delete a webhook for the Trello board."""

        if board_id is None:
            board_id = self.board_id

        logging.debug("Deleting webhook for board ID %s", board_id)

        hooks = self.client.list_hooks()
        # search and delete the webhook
        for hook in hooks:
            if hook.callback_url == callback_url and hook.id_model == self.board_id:
                hook.delete()
                logging.info("Webhook deleted successfully with ID %s", hook.id)
                return

        logging.error(
            "Failed to delete webhook for board ID %s callback_url %s",
            board_id,
            callback_url,
        )
        raise exceptions.ResourceUnavailable(
            "Failed to delete webhook, not found", HttpResponse(status_code=404)
        )

    def get_list_id(self, list_name, board_id=None):
        """Get the list id from a list name."""

        if board_id is None:
            board_id = self.board_id

        logging.debug("Getting list ID for list name %s", list_name)

        board = self.client.get_board(board_id)
        lists = board.list_lists()

        for list_ in lists:
            if list_.name.lower() == list_name.lower():
                logging.info("List ID: %s, List Name: %s", list_.id, list_.name)
                return list_.id

        logging.error("No list found with the name %s", list_name)
        raise exceptions.ResourceUnavailable(
            f"No list found with the name {list_name}", 404
        )

    class TrelloData(BaseModel):
        """Trello webhook data."""

        action: Dict
        model: Optional[Dict] = None


@click.group()
@click.option(
    "--board-name",
    required=True,
    help="The name of the Trello board to create a webhook for.",
    default=os.environ.get("TRELLO_BOARD_NAME"),
)
@click.pass_context
def cli(ctx, board_name):
    """Trello CLI."""

    ctx.ensure_object(dict)
    trello_client = FlockTrelloClient(board_name)
    ctx.obj["flock_trello"] = trello_client
    init_logging(level="CRITICAL")


@click.command()
@click.option(
    "--callback-url",
    required=True,
    help="The URL to call when the webhook is triggered.",
    default=os.environ.get("CALLBACK_URL"),
)
@click.pass_context
def create_trello_webhook(ctx, callback_url):
    """Create a webhook for the Trello board."""

    flock_trello: FlockTrelloClient = ctx.obj["flock_trello"]
    flock_trello.create_trello_webhook(
        callback_url=callback_url, board_id=flock_trello.board_id
    )
    click.echo(
        f"Board ID: {flock_trello.board_id} Callback URL: {callback_url} created"
    )


@click.command()
@click.option(
    "--callback-url",
    required=True,
    help="The URL to call when the webhook is triggered.",
    default=os.environ.get("CALLBACK_URL"),
)
@click.pass_context
def delete_trello_webhook(ctx, callback_url):
    """Delete a webhook for the Trello board."""

    trello_client: FlockTrelloClient = ctx.obj["flock_trello"]
    trello_client.delete_trello_webhook(
        callback_url=callback_url, board_id=trello_client.board_id
    )


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

    trello_client: FlockTrelloClient = ctx.obj["flock_trello"]
    trello_client.get_list_id(list_name)


cli.add_command(create_trello_webhook)
cli.add_command(delete_trello_webhook)
cli.add_command(get_list_id)

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
