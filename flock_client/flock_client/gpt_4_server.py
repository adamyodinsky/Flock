import os
from typing import Dict, List, Optional

from fastapi import FastAPI
from gpt4all import GPT4All
from pydantic import BaseModel
from uvicorn import run


class Request(BaseModel):
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
    object: str
    model: str
    choices: List[Dict]
    usage: Dict


gpt = GPT4All(
    model_name="ggml-gpt4all-l13b-snoozy",
    model_path="/Users/adamyodinsky/.flock/models/",
    model_type="llama",
)

app = FastAPI()


@app.post("/v1/chat/completions")
async def agent_endpoint(req: Request):
    """Endpoint for the agent to call for inference."""

    # TODO: pass config to chat_completion - **req.dict(exclude={"messages"})
    answer = gpt.chat_completion(messages=req.messages)

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


host = os.environ.get("FLOCK_GPT4ALL_HOST", "localhost")
port = int(os.environ.get("FLOCK_GPT4ALL_PORT", "8080"))

print(f"Starting server on {host}:{port}")

run(app, host=host, port=port, log_level="warning")
