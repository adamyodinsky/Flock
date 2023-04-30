# coding: utf-8

# from typing import Dict, List  # noqa: F401
# from fastapi import Form  # noqa: F401
from typing import Union

from fastapi import (  # Cookie,; Depends,; Header,; Query,; Response,; Security,; status,
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
)
from flock_models.builder import ResourceBuilder
from flock_resource_store.mongo import ResourceStore
from flock_schemas import SchemasFactory
from pydantic import ValidationError

from server.models.resource_details import ResourceDetails
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


def get_router(
    resource_store: ResourceStore, resource_builder: ResourceBuilder
) -> APIRouter:
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
        try:
            resource_data = resource_store.get(
                namespace=namespace, kind=kind, name=name
            )
            if resource_data is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Resource not found",
                        f"Parameters: {namespace}/{kind}/{name}",
                    ],
                )
            schema_instance = SchemasFactory.get_schema(kind).validate(resource_data)
            return ResourceFetched(data=schema_instance)
        except ValidationError as error:
            raise HTTPException(
                status_code=500,
                detail=[
                    "Resource is not valid",
                    str(error),
                ],
            ) from error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get resource",
                    str(error),
                ],
            ) from error

    @router.get(
        "/resource/{namespace}/{kind}",
        responses={
            200: {"model": ResourcesFetched, "description": "Resources Fetched"},
            400: {"model": ResourceBadRequest, "description": "Resource Bad Request"},
            404: {"model": ResourceNotFound, "description": "Resource Not Found"},
            500: {"model": InternalServerError, "description": "Internal Server Error"},
        },
        tags=["flock"],
        summary="get-resource-namespace-kind",
        response_model_by_alias=True,
    )
    async def get_resource_namespace_kind(
        namespace: str = Path(..., description="namespace"),
        kind: str = Path(..., description="kind"),
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourcesFetched:
        """Get Resources list by namespace and kind"""
        try:
            resource_data = resource_store.get_many(namespace=namespace, kind=kind)
            if resource_data is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Resource not found",
                        f"Parameters: {namespace}/{kind}",
                    ],
                )
            schema_instances = [
                ResourceDetails.validate(item) for item in resource_data  # type: ignore
            ]
            return ResourcesFetched(data=schema_instances)
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get resource",
                    str(error),
                ],
            ) from error

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

    @router.delete(
        path="/resource/{namespace}/{kind}/{name}",
        responses={
            # 204: {"model": ResourceDeleted, "description": "Resource Deleted"},
            400: {"model": ResourceBadRequest, "description": "Resource Bad Request"},
            404: {"model": ResourceNotFound, "description": "Resource Not Found"},
            500: {"model": InternalServerError, "description": "Internal Server Error"},
        },
        tags=["default"],
        summary="delete-resource-namespace-kind-name",
        response_model_by_alias=True,
    )
    async def delete_resource_namespace_kind_name(
        namespace: str = Path(..., description="Namespace of resource"),
        kind: str = Path(..., description="Kind of resource"),
        name: str = Path(..., description="Name of a resource"),
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceDeleted:
        """Deletes a resource by namespace, kind and name."""

        try:
            resource_data = resource_store.delete(
                namespace=namespace, kind=kind, name=name
            )
            return ResourceDeleted(
                details=[
                    "Resource deleted",
                    f"Parameters: {namespace}/{kind}/{name}",
                    f"Count: {resource_data.count}",
                ],
            )
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to delete resource",
                    str(error),
                ],
            ) from error

    @router.put(
        path="/resource",
        responses={
            202: {"model": ResourceAccepted, "description": "Resource Accepted"},
            200: {"model": ResourceUpdated, "description": "Resource Updated"},
            400: {"model": ResourceBadRequest, "description": "Resource Bad Request"},
            409: {
                "model": ResourceAlreadyExists,
                "description": "Resource Already Exists",
            },
            500: {"model": InternalServerError, "description": "Internal Server Error"},
        },
        tags=["flock"],
        summary="put-resource",
        response_model_by_alias=True,
    )
    async def put_resource(
        # namespace: str = Path(..., description="Namespace of resource"),
        # kind: str = Path(..., description="Kind of resource"),
        # name: str = Path(..., description="Name of a resource"),
        resource_data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceUpdated:
        """Create or update a resource"""

        # try:
        #     assert namespace == resource_data["namespace"]
        #     assert kind == resource_data["kind"]
        #     assert name == resource_data["metadata"]["name"]
        # except AssertionError as error:
        #     raise HTTPException(
        #         status_code=400,
        #         detail=[
        #             "Resource data does not match parameters",
        #             f"Parameters: {namespace}/{kind}/{name}",
        #             f"Schema: {resource_data['namespace']}/{resource_data['kind']}/{resource_data['metadata']['name']}",
        #         ],
        #     ) from error

        try:
            # validate resource building
            schema_instance = SchemasFactory.get_schema(resource_data["kind"]).validate(
                resource_data
            )
            resource_builder.build_resource(resource_data)
        except ValidationError as error:
            raise HTTPException(
                status_code=400,
                detail=["Failed to build resource", str(error)],
            ) from error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=["Failed to build resource", str(error)],
            ) from error

        # store resource
        try:
            resource_store.put(val=schema_instance.dict(by_alias=True))
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return ResourceUpdated(data=schema_instance)

    return router
