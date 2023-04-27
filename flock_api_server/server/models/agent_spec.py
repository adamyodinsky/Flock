# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from server.models.agent_type import AgentType
from server.models.base_tool_dependency import BaseToolDependency


class AgentSpec(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    AgentSpec - a model defined in OpenAPI

        options: The options of this AgentSpec [Optional].
        vendor: The vendor of this AgentSpec.
        tools: The tools of this AgentSpec.
        dependencies: The dependencies of this AgentSpec.
    """

    options: Optional[Dict[str, Any]] = Field(alias="options", default=None)
    vendor: AgentType = Field(alias="vendor")
    tools: List[BaseToolDependency] = Field(alias="tools")
    dependencies: List[object] = Field(alias="dependencies")

AgentSpec.update_forward_refs()
