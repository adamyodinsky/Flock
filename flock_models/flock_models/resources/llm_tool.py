"""Resource for vectorstore."""

from typing import Optional, cast, List, Dict

from flock_schemas import LLMToolSchema
from flock_schemas.base import Kind
from langchain import LLMChain
from langchain.agents import Tool as ToolWarperLC
from langchain.prompts.base import BasePromptTemplate as BasePromptTemplate
from langchain.schema import BaseLanguageModel as LCBaseLanguageModel

from flock_models.resources.base import Resource, ToolResource


class LLMToolResource(ToolResource):
    """Class for llm tool."""

    VENDORS = {"LLMChain": LLMChain}

    def __init__(
        self,
        manifest: LLMToolSchema,
        dependencies: Optional[Dict[str, Resource]],
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(manifest, dependencies)

        if tools is None:
            tools = []

        self.vendor_cls: LLMChain = cast(LLMChain, self.VENDORS[self.vendor])
        self.llm: LCBaseLanguageModel = self.dependencies[Kind.LLM].resource
        self.prompt_template: BasePromptTemplate = self.dependencies[
            Kind.PromptTemplate
        ].resource

        self.tool_function = self.vendor_cls(
            llm=self.llm, prompt=self.prompt_template, **self.options  # type: ignore
        )

        self.resource = ToolWarperLC(
            name=self.name,
            description=self.description,
            func=self.tool_function,
        )
