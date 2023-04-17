"""Base class for all resources."""

import abc


class Resource():
    """Base class for all resources."""

    def save_to_store(self, store):
        """Save resource to store."""
        

    def load_from_store(self, store):
        """Load resource from store."""    
    

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