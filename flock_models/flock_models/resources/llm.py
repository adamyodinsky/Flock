"""Interface for LLM models."""

from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseLanguageModel

from flock_models.resources.base import Resource
from flock_models.schemes.base import FlockBaseSchema


class LLMResource(Resource):
    """Class for LLM resources."""

    VENDORS = {
        "ChatOpenAI": ChatOpenAI,
    }

    def __init__(
        self,
        manifest: FlockBaseSchema,
    ):
        super().__init__(manifest)
        llm_cls: BaseLanguageModel = self.VENDORS[self.vendor]
        self.resource = llm_cls(**self.options)
