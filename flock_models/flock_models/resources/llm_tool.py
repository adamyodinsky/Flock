"""Resource for vectorstore."""

from typing import Any

from flock_schemas import LLMToolSchema
from flock_schemas.base import BaseFlockSchema, Kind
from langchain.agents import Tool as ToolWarperLC
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel
from langchain import LLMChain
from langchain.prompts.base import BasePromptTemplate as BasePromptTemplate


from flock_models.resources.base import ToolResource


class LLMToolResource(ToolResource):
    """Class for llm tool."""

    VENDORS = {"LLMChain": LLMChain}

    def __init__(
        self,
        manifest: LLMToolSchema,
        dependencies: dict[str, Any],
        tools: list[Any] = [],
    ):
        super().__init__(manifest, dependencies)
        self.vendor_cls: LLMChain = self.VENDORS[self.vendor]
        self.llm: LCBaseLanguageModel = self.dependencies[Kind.LLM]
        self.prompt_template: BasePromptTemplate = self.dependencies[Kind.PromptTemplate]

        self.tool_function = self.vendor_cls(
            llm=self.llm,
            prompt=self.prompt_template,
            **self.options,
        )

        self.resource = ToolWarperLC(
            name=self.name,
            description=self.description,
            func=self.tool_function,
        )
