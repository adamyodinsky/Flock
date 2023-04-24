from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    status_code: int


class NotFoundErrorResponse(ErrorResponse):
    status_code: int = 404


class BadRequestErrorResponse(ErrorResponse):
    status_code: int = 400


class InternalServerErrorResponse(ErrorResponse):
    status_code: int = 500


class AgentRequest(BaseModel):
    msg: str


class AgentResponse(BaseModel):
    data: str
    status_code: int = 200


class ShutdownRequest(BaseModel):
    countdown: int
    message: str
