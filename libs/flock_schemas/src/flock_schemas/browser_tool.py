from typing import Literal, Union

from pydantic import Field

from flock_schemas.base import BaseResourceSchema, BaseSpec, Category
from flock_schemas.dependencies import LLMChatDependency, LLMDependency



class BrowserToolVendor(str, Enum):
    """Enum for Agent types."""

    ZERO_SHOT_REACT_DESCRIPTION = "zero-shot-react-description"
    REACT_DOCSTORE = "react-docstore"
    SELF_ASK_WITH_SEARCH = "self-ask-with-search"
    CONVERSATIONAL_REACT_DESCRIPTION = "conversational-react-description"
    CHAT_ZERO_SHOT_REACT_DESCRIPTION = "chat-zero-shot-react-description"
    CHAT_CONVERSATIONAL_REACT_DESCRIPTION = "chat-conversational-react-description"
    STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION = (
        "structured-chat-zero-shot-react-description"
    )
    OPENAI_FUNCTIONS = "openai-functions"


class BrowserToolSpec(BaseSpec):
    """BrowserTool spec."""

    dependencies: tuple[Union[LLMDependency, LLMChatDependency]] = Field(
        ..., description="Tool dependencies"
    )


class BrowserToolSchema(BaseResourceSchema):
    """BrowserTool schema."""

    kind: Literal["BrowserTool"] = Field(..., description="The kind of the object")
    category: Category = Field(
        default=Category.TOOL, description="The resource category"
    )
    spec: BrowserToolSpec


export = {
    "sub": {
        "BrowserToolSpec": BrowserToolSpec,
    },
    "main": {
        "BrowserTool": BrowserToolSchema,
    },
}
