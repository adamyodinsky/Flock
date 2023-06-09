"""Base class for all resources."""


from typing import Any, List, Optional, cast

from langchain.agents import Tool as ToolWarperLC

from schemas.agent import AgentSchema
from schemas.base import BaseFlockSchema
from schemas.base import BaseOptions as BaseOptionsSchema
from schemas.custom import CustomSchema


class Resource:
    """Base class for all resources.

    Args:
        manifest (BaseFlockSchema): Manifest of the resource.
        dependencies (Optional[dict[str, Resource]], optional): Dependencies of the resource. Defaults to None.
        tools (Optional[List[Any]], optional): Tools of the resource. Defaults to None.

    Attributes:
        manifest (BaseFlockSchema): Manifest of the resource.
        dependencies (dict[str, Resource]): Dependencies of the resource.
        tools (List[Any]): Tools of the resource.
        vendor (str): Vendor of the resource.
        options (BaseOptionsSchema): Options of the resource.
        resource (Any): Resource object.
    """

    def __init__(
        self,
        manifest: BaseFlockSchema,
        dependencies: Optional[dict[str, Any]] = None,
        tools: Optional[List[Any]] = None,
    ):
        if dependencies is None:
            dependencies = {}
        if tools is None:
            tools = []

        self.manifest = manifest
        self.tools = tools
        self.vendor = self.manifest.spec.vendor
        self.dependencies: dict[str, Any] = dependencies
        self.options: BaseOptionsSchema = cast(BaseOptionsSchema, manifest.spec.options)
        self.resource = None


class ToolResource(Resource):
    """Base class for all tools.

    Attributes:
        name (str): Name of the tool.
        description (str): Description of the tool.
    """

    def __init__(
        self,
        manifest: BaseFlockSchema,
        dependencies: Optional[dict[str, Resource]] = None,
    ):
        super().__init__(manifest, dependencies)

        if getattr(manifest.metadata.annotations, "name", False):
            self.name: str = manifest.metadata.annotations["name"]
        else:
            self.name: str = manifest.metadata.name

        if getattr(manifest.metadata.annotations, "description", False):
            self.description: str = manifest.metadata.annotations["description"]
        else:
            self.description: str = manifest.metadata.description


class Agent(Resource):
    """Base class for all agents."""

    def __init__(
        self,
        manifest: AgentSchema,
        dependencies: Optional[dict[str, Resource]] = None,
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(
            manifest=manifest,
            dependencies=dependencies,
            tools=tools,
        )

        if getattr(manifest.metadata.annotations, "name", False):
            self.name: str = manifest.metadata.annotations["name"]
        else:
            self.name: str = manifest.metadata.name

        if getattr(manifest.metadata.annotations, "description", False):
            self.description: str = manifest.metadata.annotations["description"]
        else:
            self.description: str = manifest.metadata.description

        if tools is None:
            tools = []

        self.tools: List[ToolResource] = tools
        self.agent_tools: List[ToolWarperLC] = cast(
            List[ToolWarperLC], [tool.resource for tool in self.tools]
        )
        self.run = None


class CustomResource(Resource):
    """Base class for all agents."""

    def __init__(
        self,
        manifest: CustomSchema,
        dependencies: Optional[dict[str, Resource]] = None,
        tools: Optional[List[ToolResource]] = None,
    ):
        super().__init__(
            manifest=manifest,
            dependencies=dependencies,
            tools=tools,
        )

        if tools is None:
            tools = []

        self.tools: List[ToolResource] = tools
        self.agent_tools: List[ToolWarperLC] = cast(
            List[ToolWarperLC], [tool.resource for tool in self.tools]
        )
        self.run = None


export = {}
