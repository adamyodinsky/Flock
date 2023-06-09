"""Resource for vectorstore."""

from typing import Dict, List, Optional, cast

from langchain import LLMChain
from langchain.agents import Tool as ToolWarperLC
from langchain.base_language import BaseLanguageModel as LCBaseLanguageModel
from langchain.prompts.base import BasePromptTemplate as BasePromptTemplate

from flock_resources.base import Resource, ToolResource
from flock_schemas.llm_tool import LLMToolSchema
from flock_schemas.base import Kind


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

        self.llm = self.dependencies.get(Kind.LLM) or self.dependencies.get(
            Kind.LLMChat
        )

        self.vendor_cls = cast(LLMChain, self.VENDORS[self.vendor])

        self.prompt_template: BasePromptTemplate = self.dependencies[
            Kind.PromptTemplate
        ].resource

        self.tool_function = self.vendor_cls(
            llm=self.llm.resource, prompt=self.prompt_template, **self.options  # type: ignore
        )

        self.resource = ToolWarperLC(
            name=self.name,
            description=self.description,
            func=self.tool_function,
        )


export = {
    "LLMTool": LLMToolResource,
}
