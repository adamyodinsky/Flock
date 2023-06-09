import os
from typing import Dict, List, Optional

import click
from fastapi import FastAPI
from flock_common.env_checker import check_env_vars
from gpt4all import GPT4All
from pydantic import BaseModel
from uvicorn import run


class Request(BaseModel):
    """Request model for the chat endpoint."""

    messages: List[Dict]
    model: str
    temperature: Optional[float]
    top_p: Optional[float]
    top_k: Optional[int]
    max_tokens: Optional[int]
    batch: Optional[int]
    repeat_penalty: Optional[float]
    repeat_penalty_tokens: Optional[int]


class Response(BaseModel):
    """Response model for the chat endpoint."""

    object: str
    model: str
    choices: List[Dict]
    usage: Dict


app = FastAPI()

llm = GPT4All(
    model_name="ggml-gpt4all-l13b-snoozy",
    model_path="/Users/adamyodinsky/.flock/models/",
    model_type="llama",
)


@app.post("/v1/chat/completions")
async def chat(req: Request):
    """Endpoint for the agent to call for inference."""

    # TODO: pass config to chat_completion - **req.dict(exclude={"messages"})
    answer = llm.chat_completion(messages=req.messages)

    try:
        bot_message = answer.get("choices", [{}])[0].get("message", {}).get("content", "")  # type: ignore
    except Exception as error:
        bot_message = str(error)

    return Response(
        object="chat.completion",
        model=req.model,
        choices=[{"message": {"role": "assistant", "content": bot_message}}],
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    )


@click.group()
def cli():
    """Flock Client CLI"""

    required_vars = []
    optional_vars = [
        "HOST",
        "PORT",
    ]

    check_env_vars(required_vars, optional_vars)


@cli.command(help="Run the client server.")
@click.option(
    "--host",
    default=os.environ.get("HOST", "127.0.0.1"),
    help="The host address to bind the server to.",
)
@click.option(
    "--port",
    default=os.environ.get("PORT", 7860),
    type=int,
    help="The port the server should listen on.",
)
@click.option(
    "--log_level",
    default=os.environ.get("LOG_LEVEL", "warning"),
    type=str,
    help="The log level for the server.",
)
def serve(host, port, log_level):
    """Run the server."""

    print(f"Starting server on {host}:{port}")

    # TODO: pass manifest of an LLM to the LLM as a service engine GPT4All (for now)
    # from there it will get the path of the model, the model name and the model type
    # it can get type from annotations
    # llm = GPT4All(
    #     model_name="ggml-gpt4all-l13b-snoozy",
    #     model_path="/Users/adamyodinsky/.flock/models/",
    #     model_type="llama",
    # )
    run(app, host=host, port=port, log_level=log_level)
