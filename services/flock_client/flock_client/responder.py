"""This module contains the function that is called when the user presses submit."""

import time

import requests
from gpt4all import GPT4All

gpt = GPT4All(
    model_name="ggml-gpt4all-l13b-snoozy",
    model_path="/Users/adamyodinsky/.flock/models/",
    model_type="llama",
)


class Responder:
    """This class contains the function that is called when the user presses submit."""

    def __init__(self, backend, backend_type, model) -> None:
        self.backend = backend
        self.backend_type = backend_type
        self.model = model

    @staticmethod
    def user(user_message, chat_history):
        """This function is called when the user presses submit."""
        return "", chat_history + [["user", user_message]]

    def get_agent_responder(self):
        """Returns the responder function."""

        def responder(user_message, chat_history):
            """This function is called when the user presses submit."""

            user_message = chat_history[-1][1]
            try:
                response = requests.post(
                    self.backend,
                    json={"msg": user_message},
                    timeout=None,
                ).json()
                bot_message = response["data"]
            except requests.exceptions.Timeout as error:
                bot_message = f"{str(error)}"

            chat_history.append(("assistant", bot_message))
            return "", chat_history

        return responder

    def get_llama_responder(self):
        """Returns the responder function."""

        def responder(user_message, chat_history):
            """This function is called when the user presses submit."""

            messages = self._tuple_to_dict(chat_history)

            try:
                response = requests.post(
                    self.backend,
                    json={
                        "messages": messages,
                        "model": self.model,
                        "temperature": 0.28,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_tokens": 4096,
                        "batch": 9,
                        "repeat_penalty": 1.1,
                        "repeat_penalty_tokens": 60,
                    },
                    timeout=None,
                ).json()
                bot_message = (
                    response.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )
            except requests.exceptions.Timeout as error:
                bot_message = f"{str(error)}"

            chat_history.append(("assistant", bot_message))
            return "", chat_history

        return responder

    def get_responder(self):
        """Returns the responder function."""
        if self.backend_type == "agent":
            return self.get_agent_responder()
        elif self.backend_type == "llm":
            return self.get_llama_responder()
        else:
            raise ValueError(f"Unknown bself.ackend type: {self.backend_type}")

    def _dict_to_tuple(self, chat_history):
        """Convert a list of dictionaries to a list of tuples."""
        return [(list(item.keys())[0], list(item.values())[0]) for item in chat_history]

    def _tuple_to_dict(self, chat_history):
        """Convert a list of tuples to a list of dictionaries."""
        return [{"role": item[0], "content": item[1]} for item in chat_history]

    def _stream_output(self, history, bot_message):
        """This function is called when the user presses submit."""

        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            time.sleep(0.05)
            yield history
