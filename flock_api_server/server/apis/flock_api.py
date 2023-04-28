# coding: utf-8

# from typing import Dict, List  # noqa: F401
# from fastapi import Form  # noqa: F401
from fastapi import (  # Cookie,; Depends,; Header,; Query,; Response,; Security,; status,
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
)
from flock_resource_store.mongo import MongoResourceStore, ResourceStore

from server.models.responses.internal_server_error import InternalServerError
from server.models.responses.resource_accepted import ResourceAccepted
from server.models.responses.resource_already_exists import ResourceAlreadyExists
from server.models.responses.resource_bad_request import ResourceBadRequest
from server.models.responses.resource_created import ResourceCreated
from server.models.responses.resource_deleted import ResourceDeleted
from server.models.responses.resource_fetched import ResourceFetched
from server.models.responses.resource_not_found import ResourceNotFound
from server.models.responses.resource_updated import ResourceUpdated
from server.models.responses.resources_fetched import ResourcesFetched

# from server.modelsextra_models import TokenModel  # noqa: F401


def get_router(resource_store: MongoResourceStore) -> APIRouter:
    """Get API router"""

    router = APIRouter()

    @router.get(
        "/resource/{namespace}/{kind}/{name}",
        responses={
            200: {"model": ResourceFetched, "description": "Resource Fetched"},
            404: {"model": ResourceNotFound, "description": "Resource Not Found"},
            500: {"model": InternalServerError, "description": "Internal Server Error"},
        },
        tags=["flock"],
        summary="get-resource",
        response_model_by_alias=True,
    )
    async def get_resource(
        namespace: str = Path(..., description="Namespace of resource"),
        kind: str = Path(..., description="Kind of resource"),
        name: str = Path(..., description="Name of a resource"),
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceFetched:
        """Get a resource"""
        resource = resource_store.get(f"{namespace}/{kind}/{name}")
        if resource is None:
            raise HTTPException(
                status_code=404,
                detail=f"Did not find {namespace}/{kind}/{name}",
            )
        return ResourceFetched(data=resource)

    # @router.get(
    #     "/resource/{namespace}/{kind}",
    #     responses={
    #         200: {"model": ResourcesFetched, "description": "Resources Fetched"},
    #         400: {"model": ResourceBadRequest, "description": "Resource Bad Request"},
    #         404: {"model": ResourceNotFound, "description": "Resource Not Found"},
    #         500: {"model": InternalServerError, "description": "Internal Server Error"},
    #     },
    #     tags=["flock"],
    #     summary="get-resource-namespace-kind",
    #     response_model_by_alias=True,
    # )
    # async def get_resource_namespace_kind(
    #     namespace: str = Path(None, description="namespace"),
    #     kind: str = Path(None, description="kind"),
    # ) -> ResourcesFetched:
    #     """Get Resources list by namespace and kind"""
    #     resources = resource_store.get_many(f"{namespace}/{kind}")
    #     if resources is None:
    #         raise ResourceNotFound(
    #             details=["Did not find", f"{namespace}/{kind}"],
    #         )
    #     return ResourcesFetched(data=resources)

    # @router.delete(
    #     "/resource/{namespace}/{kind}",
    #     responses={
    #         200: {"model": ResourcesFetched, "description": "Resources Fetched"},
    #         400: {"model": ResourceBadRequest, "description": "Resource Bad Request"},
    #         404: {"model": ResourceNotFound, "description": "Resource Not Found"},
    #         500: {"model": InternalServerError, "description": "Internal Server Error"},
    #     },
    #     tags=["default"],
    #     summary="delete-resource-namespace-kind",
    #     response_model_by_alias=True,
    # )
    # async def delete_resource_namespace_kind(
    #     namespace: str = Path(None, description="namespace"),
    #     kind: str = Path(None, description="kind"),
    # ) -> ResourcesFetched:
    #     """Deletes all resources by namespace and kind, returns a list of the deleted resources."""
    #     ...

    # @router.delete(
    #     "/resource/{namespace}/{kind}/{name}",
    #     responses={
    #         204: {"model": ResourceDeleted, "description": "Resource Deleted"},
    #         400: {"model": ResourceBadRequest, "description": "Resource Bad Request"},
    #         404: {"model": ResourceNotFound, "description": "Resource Not Found"},
    #         500: {"model": InternalServerError, "description": "Internal Server Error"},
    #     },
    #     tags=["default"],
    #     summary="delete-resource-namespace-kind-name",
    #     response_model_by_alias=True,
    # )
    # async def delete_resource_namespace_kind_name(
    #     namespace: str = Path(None, description="Namespace of resource"),
    #     kind: str = Path(None, description="Kind of resource"),
    #     name: str = Path(None, description="Name of a resource"),
    # ) -> ResourceDeleted:
    #     """Delete a resource and returns it"""
    #     ...

    # @router.post(
    #     "/resource/{namespace}/{kind}/{name}",
    #     responses={
    #         201: {"model": ResourceCreated, "description": "Resource Created"},
    #         202: {"model": ResourceAccepted, "description": "Resource Accepted"},
    #         400: {"model": ResourceBadRequest, "description": "Resource Bad Request"},
    #         409: {
    #             "model": ResourceAlreadyExists,
    #             "description": "Resource Already Exists",
    #         },
    #         500: {"model": InternalServerError, "description": "Internal Server Error"},
    #     },
    #     tags=["default"],
    #     summary="post-resource",
    #     response_model_by_alias=True,
    # )
    # async def post_resource(
    #     namespace: str = Path(None, description="Namespace of resource"),
    #     kind: str = Path(None, description="Kind of resource"),
    #     name: str = Path(None, description="Name of a resource"),
    #     resource_data: ResourceData = Body(None, description=""),
    # ) -> ResourceCreated:
    #     """Create a resource"""
    #     ...

    @router.put(
        "/resource/{namespace}/{kind}/{name}",
        responses={
            201: {"model": ResourceCreated, "description": "Resource Created"},
            202: {"model": ResourceAccepted, "description": "Resource Accepted"},
            # 204: {"model": ResourceUpdated, "description": "Resource Updated"},
            400: {"model": ResourceBadRequest, "description": "Resource Bad Request"},
            409: {
                "model": ResourceAlreadyExists,
                "description": "Resource Already Exists",
            },
            500: {"model": InternalServerError, "description": "Internal Server Error"},
        },
        tags=["default"],
        summary="put-resource",
        response_model_by_alias=True,
    )
    async def put_resource(
        namespace: str = Path(..., description="Namespace of resource"),
        kind: str = Path(..., description="Kind of resource"),
        name: str = Path(..., description="Name of a resource"),
        resource_data: object = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceCreated:
        """Create or update a resource"""
        # try:
        #     assert namespace == resource_data.namespace
        #     assert kind == resource_data.kind
        #     assert name == resource_data.name
        # except AssertionError:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Path parameters do not match resource data",
        #     )
        resource_store.put(
            key=f"{resource_data['namespace']}/{resource_data['kind']}/{resource_data['name']}",
            val=resource_data,
        )
        return ResourceCreated(data=resource_data)

    return router
