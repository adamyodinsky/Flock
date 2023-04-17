"""Interface for LLM models."""

from flock_models.schemes.llm import LLMSchema
from flock_models.resources.base import Resource
from langchain.schema import BaseLanguageModel
from flock_store.secrets.base import SecretStore


class LLMResource(Resource):
    """Class for LLM resources."""

    def __init__(self, manifest: LLMSchema, llm: BaseLanguageModel):
        self.manifest: LLMSchema = LLMSchema(**manifest)
        self.resource: BaseLanguageModel = llm(**self.manifest.spec.options.dict())

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
