"""Interface for LLM models."""

from typing import List, Optional, cast

from langchain.base_language import BaseLanguageModel

# TODO: waiting for GPT4All langchain to be updated, pygpt4all is not supported anymore.
from langchain.llms.gpt4all import GPT4All

from flock_resources.base import Resource, ToolResource
from flock_schemas.llm import LLMSchema


class LLMResource(Resource):
    """Class for LLM resources."""

    VENDORS = {
        "GPT4All": GPT4All,
    }

    def __init__(
        self,
        manifest: LLMSchema,
        dependencies: Optional[dict[str, Resource]] = None,
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest)
        self.vendor_cls: BaseLanguageModel = cast(
            BaseLanguageModel, self.VENDORS[self.vendor]
        )

        self.resource = self.vendor_cls(**self.options)  # type: ignore


export = {
    "LLM": LLMResource,
}
