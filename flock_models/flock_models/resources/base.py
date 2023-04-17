"""Base class for all resources."""


from typing import Any


class Resource:
    """Base class for all resources."""

    def __init__(
        self,
        vendor: str,
        options: dict[str, Any],
        dependencies: dict[str, Any],
    ):
        self.vendor = vendor
        self.options = options
        self.dependencies = dependencies
        self.resource = None


class ToolResource(Resource):
    """Base class for all tools."""

    def get_func(self):
        """Get function of tool."""
        pass

    def get_name(self) -> str:
        """Get name of tool."""
        pass

    def get_description(self) -> str:
        """Get description of tool."""
        pass


class Agent(Resource):
    """Base class for all agents."""
