"""Interface for LLM models."""

from typing import Any
from flock_models.schemes.llm import LLMSchema
from flock_models.resources.base import Resource
from langchain.schema import BaseLanguageModel
from flock_store.secrets.base import SecretStore


class LLMResource(Resource):
    """Base class for embedding resources."""

    def __init__(self, manifest: dict[str, Any], llm: BaseLanguageModel):
        super().__init__(manifest, LLMSchema)
        self.resource = llm(**self.manifest.spec.options.dict())

    def set_api_token(self, key, secret_name: str, secret_store: SecretStore):
        self.resource[key] = secret_store.get(secret_name)


# ---
# apiVersion: flock/v1
# kind: LLM
# # uuid: b70bb61d-6710-48bd-85b0-f32c91f1eed1
# metadata:
#   name: my-openai-llm
#   description: openai language model
#   labels:
#     app: my_app
# spec:
#   vendor: openai
#   options:
#       model: gpt3.5-turbo
#       token_limit: 1000
#       temperature: 0.5
