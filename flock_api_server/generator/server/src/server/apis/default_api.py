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

from server.models.resource_accepted import ResourceAccepted
from server.models.resource_created import ResourceCreated
from server.models.resource_updated import ResourceUpdated
from server.models.resources_fetched import ResourcesFetched
from server.schemas.extra_models import TokenModel  # noqa: F401
from server.schemas.internal_server_error import InternalServerError1
from server.schemas.resource_bad_request import ResourceBadRequest1
from server.schemas.resource_data import ResourceData
from server.schemas.resource_not_found import ResourceNotFound1
from server.schemas.responses.resource_already_exists import ResourceAlreadyExists1
from server.schemas.responses.resource_deleted import ResourceDeleted

router = APIRouter()


@router.delete(
    "/resource/{namespace}/{kind}",
    responses={
        200: {"model": ResourcesFetched, "description": "Resources Fetched"},
        400: {"model": ResourceBadRequest1, "description": "Resource Bad Request"},
        404: {"model": ResourceNotFound1, "description": "Resource Not Found"},
        500: {"model": InternalServerError1, "description": "Internal Server Error"},
    },
    tags=["default"],
    summary="delete-resource-namespace-kind",
    response_model_by_alias=True,
)
async def delete_resource_namespace_kind(
    namespace: str = Path(None, description="namespace"),
    kind: str = Path(None, description="kind"),
) -> ResourcesFetched:
    """Deletes all resources by namespace and kind, returns a list of the deleted resources."""
    ...


@router.delete(
    "/resource/{namespace}/{kind}/{name}",
    responses={
        204: {"model": ResourceDeleted, "description": "Resource Deleted"},
        400: {"model": ResourceBadRequest1, "description": "Resource Bad Request"},
        404: {"model": ResourceNotFound1, "description": "Resource Not Found"},
        500: {"model": InternalServerError1, "description": "Internal Server Error"},
    },
    tags=["default"],
    summary="delete-resource-namespace-kind-name",
    response_model_by_alias=True,
)
async def delete_resource_namespace_kind_name(
    namespace: str = Path(None, description="Namespace of resource"),
    kind: str = Path(None, description="Kind of resource"),
    name: str = Path(None, description="Name of a resource"),
) -> ResourceDeleted:
    """Delete a resource and returns it"""
    ...


@router.post(
    "/resource/{namespace}/{kind}/{name}",
    responses={
        201: {"model": ResourceCreated, "description": "Resource Created"},
        202: {"model": ResourceAccepted, "description": "Resource Accepted"},
        400: {"model": ResourceBadRequest1, "description": "Resource Bad Request"},
        409: {
            "model": ResourceAlreadyExists1,
            "description": "Resource Already Exists",
        },
        500: {"model": InternalServerError1, "description": "Internal Server Error"},
    },
    tags=["default"],
    summary="post-resource",
    response_model_by_alias=True,
)
async def post_resource(
    namespace: str = Path(None, description="Namespace of resource"),
    kind: str = Path(None, description="Kind of resource"),
    name: str = Path(None, description="Name of a resource"),
    resource_data: ResourceData = Body(None, description=""),
) -> ResourceCreated:
    """Create a resource"""
    ...


@router.put(
    "/resource/{namespace}/{kind}/{name}",
    responses={
        201: {"model": ResourceCreated, "description": "Resource Created"},
        202: {"model": ResourceAccepted, "description": "Resource Accepted"},
        204: {"model": ResourceUpdated, "description": "Resource Updated"},
        400: {"model": ResourceBadRequest1, "description": "Resource Bad Request"},
        409: {
            "model": ResourceAlreadyExists1,
            "description": "Resource Already Exists",
        },
        500: {"model": InternalServerError1, "description": "Internal Server Error"},
    },
    tags=["default"],
    summary="put-resource",
    response_model_by_alias=True,
)
async def put_resource(
    namespace: str = Path(None, description="Namespace of resource"),
    kind: str = Path(None, description="Kind of resource"),
    name: str = Path(None, description="Name of a resource"),
    resource_data: ResourceData = Body(None, description=""),
) -> ResourceCreated:
    """Create or update a resource"""
    ...
