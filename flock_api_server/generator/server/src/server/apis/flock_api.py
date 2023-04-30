# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,  # noqa: F401
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from server.models.resource_fetched import ResourceFetched
from server.models.resources_fetched import ResourcesFetched
from server.schemas.extra_models import TokenModel  # noqa: F401
from server.schemas.internal_server_error import InternalServerError1
from server.schemas.resource_bad_request import ResourceBadRequest1
from server.schemas.resource_not_found import ResourceNotFound1

router = APIRouter()


@router.get(
    "/resource/{namespace}/{kind}/{name}",
    responses={
        200: {"model": ResourceFetched, "description": "Resource Fetched"},
        404: {"model": ResourceNotFound1, "description": "Resource Not Found"},
        500: {"model": InternalServerError1, "description": "Internal Server Error"},
    },
    tags=["flock"],
    summary="get-resource",
    response_model_by_alias=True,
)
async def get_resource(
    namespace: str = Path(None, description="Namespace of resource"),
    kind: str = Path(None, description="Kind of resource"),
    name: str = Path(None, description="Name of a resource"),
) -> ResourceFetched:
    """Get a resource"""
    ...


@router.get(
    "/resource/{namespace}/{kind}",
    responses={
        200: {"model": ResourcesFetched, "description": "Resources Fetched"},
        400: {"model": ResourceBadRequest1, "description": "Resource Bad Request"},
        404: {"model": ResourceNotFound1, "description": "Resource Not Found"},
        500: {"model": InternalServerError1, "description": "Internal Server Error"},
    },
    tags=["flock"],
    summary="get-resource-namespace-kind",
    response_model_by_alias=True,
)
async def get_resource_namespace_kind(
    namespace: str = Path(None, description="namespace"),
    kind: str = Path(None, description="kind"),
) -> ResourcesFetched:
    """Get Resources list by namespace and kind"""
    ...
