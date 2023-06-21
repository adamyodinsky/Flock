import os

import click
import gradio as gr
from flock_common.env_checker import check_env_vars

from flock_client.responder import Responder


@click.group()
def cli():
    """Flock Client CLI"""

    required_vars = []
    optional_vars = [
        "FLOCK_CLIENT_BACKEND_HOST",
        "FLOCK_CLIENT_BACKEND_TYPE",
        "FLOCK_CLIENT_HOST",
        "FLOCK_CLIENT_PORT",
        "FLOCK_CLIENT_BACKEND_MODEL",
    ]

    check_env_vars(required_vars, optional_vars)


@cli.command(help="Run the client server.")
@click.option(
    "--host",
    default=os.environ.get("FLOCK_CLIENT_HOST", "127.0.0.1"),
    help="The host address to bind the server to.",
)
@click.option(
    "--port",
    default=os.environ.get("FLOCK_CLIENT_PORT", 7860),
    type=int,
    help="The port the server should listen on.",
)
@click.option(
    "--backend-host",
    default=os.environ.get("FLOCK_CLIENT_BACKEND_HOST", "http://localhost:8000/agent"),
    help="The model or agent address use.",
)
@click.option(
    "--backend-type",
    default=os.environ.get("FLOCK_CLIENT_BACKEND_TYPE", "agent"),
    type=click.Choice(["agent", "llm"]),
    help="The model or agent address use.",
)
@click.option(
    "--backend-llm-model",
    default=os.environ.get(
        "FLOCK_CLIENT_BACKEND_MODEL", "ggml-gpt4all-l13b-snoozy.bin"
    ),
    help="The model or agent address use.",
)
def run_server(host, port, backend_host, backend_type, backend_llm_model):
    """Run the client server.

    Args:
        host (str): The host address to bind the server to.
        port (int): The port the server should listen on.
        backend_host (str): The model or agent address use.
        backend_type (str): The model or agent address use.
        backend_llm_model (str): The model or agent address use.
    """

    click.echo(f"Starting {backend_type} server on {host}:{port}...")

    responder_cls = Responder(
        backend=backend_host,
        backend_type=backend_type,
        model=backend_llm_model,
    )

    responder = responder_cls.get_responder()

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(label=backend_type.title())
        msg: gr.Textbox = gr.Textbox(
            label="User", placeholder="Type your message here..."
        )
        clear = gr.Button("Clear")

        msg.submit(Responder.user, [msg, chatbot], [msg, chatbot]).then(
            responder, [msg, chatbot], [msg, chatbot]
        )
        # msg.submit(responder, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    demo.launch(
        server_name=host,
        server_port=port,
    )


cli.add_command(run_server)

if __name__ == "__main__":
    cli()
