"""Status codes for the API"""

from enum import Enum

from flock_schemas import BaseResourceSchema


class Code(str, Enum):
    """HTTP status codes"""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


class Status(str, Enum):
    """Status of the response"""

    SUCCESS = "success"
    ERROR = "error"


class Message(str, Enum):
    """Message of the response"""

    FETCHED = "Resources retrieved successfully"
    CREATED = "Resource created successfully"
    NOT_FOUND = "Resource not found"
    DELETED = "Resource deleted successfully"
    UPDATED = "Resource updated successfully"
    ACCEPTED = "Resource accepted successfully"
    BAD_REQUEST = "Bad request"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    CONFLICT = "Conflict"
    INTERNAL_SERVER_ERROR = "Internal server error"


ResourceType = BaseResourceSchema
# class ResourceType(str, Enum):
#     """Resource type"""

#     AgentSchema = (flock_schemas.AgentSchema,)
#     EmbeddingSchema = (flock_schemas.EmbeddingSchema,)
#     LLMSchema = (flock_schemas.LLMSchema,)
#     LLMToolSchema = (flock_schemas.LLMToolSchema,)
#     LoadToolSchema = (flock_schemas.LoadToolSchema,)
#     PromptTemplateSchema = (flock_schemas.PromptTemplateSchema,)
#     SplitterSchema = (flock_schemas.SplitterSchema,)
#     VectorStoreSchema = (flock_schemas.VectorStoreSchema,)
#     VectorStoreQAToolSchema = (flock_schemas.VectorStoreQAToolSchema,)
#     CustomSchema = (flock_schemas.CustomSchema,)
#     BaseResourceSchema = (flock_schemas.BaseResourceSchema,)
