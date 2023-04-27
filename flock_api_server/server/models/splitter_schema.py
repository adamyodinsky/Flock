# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from server.models.agent_schema_metadata import AgentSchemaMetadata
from server.models.splitter_schema_spec import SplitterSchemaSpec


class SplitterSchema(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    SplitterSchema - a model defined in OpenAPI

        namespace: The namespace of this SplitterSchema.
        api_version: The api_version of this SplitterSchema.
        kind: The kind of this SplitterSchema.
        metadata: The metadata of this SplitterSchema.
        created_at: The created_at of this SplitterSchema [Optional].
        updated_at: The updated_at of this SplitterSchema [Optional].
        spec: The spec of this SplitterSchema.
    """

    namespace: str = Field(alias="namespace")
    api_version: str = Field(alias="apiVersion")
    kind: str = Field(alias="kind")
    metadata: AgentSchemaMetadata = Field(alias="metadata")
    created_at: Optional[datetime] = Field(alias="created_at", default=None)
    updated_at: Optional[datetime] = Field(alias="updated_at", default=None)
    spec: SplitterSchemaSpec = Field(alias="spec")

    @validator("namespace")
    def namespace_max_length(cls, value):
        assert len(value) <= 63
        return value

SplitterSchema.update_forward_refs()
