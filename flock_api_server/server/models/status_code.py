"""Status codes for the API"""

from enum import Enum


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

    SUCCESS = "Resources retrieved successfully"
    ERROR = "Error retrieving resources"
