# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401
from server.models.agent_schema import AgentSchema
from server.models.agent_schema_metadata import AgentSchemaMetadata
from server.models.agent_schema_spec import AgentSchemaSpec
from server.models.custom_schema import CustomSchema
from server.models.embedding_schema import EmbeddingSchema
from server.models.llm_schema import LLMSchema
from server.models.llm_tool_schema import LLMToolSchema
from server.models.load_tool_schema import LoadToolSchema
from server.models.prompt_template_schema import PromptTemplateSchema
from server.models.splitter_schema import SplitterSchema
from server.models.vector_store_qa_tool_schema import VectorStoreQAToolSchema
from server.models.vector_store_schema import VectorStoreSchema


class ResourceDeletedData(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ResourceDeletedData - a model defined in OpenAPI

        namespace: The namespace of this ResourceDeletedData.
        api_version: The api_version of this ResourceDeletedData.
        kind: The kind of this ResourceDeletedData.
        metadata: The metadata of this ResourceDeletedData.
        created_at: The created_at of this ResourceDeletedData [Optional].
        updated_at: The updated_at of this ResourceDeletedData [Optional].
        spec: The spec of this ResourceDeletedData.
    """

    namespace: str = Field(alias="namespace")
    api_version: str = Field(alias="apiVersion")
    kind: str = Field(alias="kind")
    metadata: AgentSchemaMetadata = Field(alias="metadata")
    created_at: Optional[datetime] = Field(alias="created_at", default=None)
    updated_at: Optional[datetime] = Field(alias="updated_at", default=None)
    spec: AgentSchemaSpec = Field(alias="spec")

    @validator("namespace")
    def namespace_max_length(cls, value):
        assert len(value) <= 63
        return value

ResourceDeletedData.update_forward_refs()
