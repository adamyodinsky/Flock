# # coding: utf-8

# from __future__ import annotations

# from datetime import datetime
# from typing import Optional, Union, cast

# import flock_schemas
# from flock_schemas import Schemas, SchemasFactory
# from pydantic import BaseModel, Field, validator


# class ResourceData:
#     """ResourceData."""

#     self = Union[
#         flock_schemas.AgentSchema,
#         flock_schemas.EmbeddingSchema,
#         flock_schemas.LLMSchema,
#         flock_schemas.LLMToolSchema,
#         flock_schemas.LoadToolSchema,
#         flock_schemas.PromptTemplateSchema,
#         flock_schemas.SplitterSchema,
#         flock_schemas.VectorStoreSchema,
#         flock_schemas.VectorStoreQAToolSchema,
#         flock_schemas.CustomSchema,
#     ]
