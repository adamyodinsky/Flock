"""Base class for all resources."""


from typing import Any

from flock_schemas import BaseFlockSchema, AgentSchema
from langchain.agents import Tool as ToolWarperLC


class Resource:
    """Base class for all resources."""

    def __init__(
        self,
        manifest: BaseFlockSchema,
        dependencies: dict[str, Any] = None,
        tools: list[ToolWarperLC] = [],
    ):
        self.vendor: str = manifest.spec.vendor
        self.options: dict[str, Any] = manifest.spec.options
        self.dependencies: dict[str, Any] = dependencies
        self.resource = None


class ToolResource(Resource):
    """Base class for all tools."""

    def __init__(self, manifest: BaseFlockSchema, dependencies: dict[str, Any] = None):
        super().__init__(manifest, dependencies)

        if getattr(manifest.metadata.annotations, "name", False):
            self.name: str = manifest.metadata.annotations.name
        else:
            self.name: str = manifest.metadata.name

        if getattr(manifest.metadata.annotations, "description", False):
            self.description: str = manifest.metadata.annotations.description
        else:
            self.description: str = manifest.metadata.description


class Agent(Resource):
    """Base class for all agents."""
    pass

    def __init__(
        self,
        manifest: AgentSchema,
        dependencies: dict[str, Any] = None,
        tools: list[ToolWarperLC] = [],
    ):
        super().__init__(manifest, dependencies)
        self.tools = tools
        self.run = None