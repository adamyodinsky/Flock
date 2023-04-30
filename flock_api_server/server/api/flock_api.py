# coding: utf-8

# from typing import Dict, List  # noqa: F401
# from fastapi import Form  # noqa: F401

from fastapi import (  # Cookie,; Depends,; Header,; Query,; Response,; Security,; status,
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from flock_models.builder import ResourceBuilder
from flock_resource_store.mongo import ResourceStore
from flock_schemas import SchemasFactory
from pydantic import ValidationError

from server.schemas.resource_details import ResourceDetails
from server.schemas.responses.resource_deleted import ResourceDeleted
from server.schemas.responses.resource_fetched import ResourceFetched
from server.schemas.responses.resource_updated import ResourceUpdated
from server.schemas.responses.resources_fetched import ResourcesFetched
from server.schemas.status_code import ResourceType

# from server.modelsextra_models import TokenModel  # noqa: F401


def get_router(
    resource_store: ResourceStore, resource_builder: ResourceBuilder
) -> APIRouter:
    """Get API router"""

    router = APIRouter()

    @router.get(
        "/resource/{namespace}/{kind}/{name}",
        response_model=ResourceFetched,
    )
    async def get_resource(
        namespace: str,
        kind: str,
        name: str,
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ):
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

    @router.get("/resource/{namespace}/{category}")
    @router.get("/resource/{namespace}/{kind}")
    async def get_resources(
        kind: str = "",
        category: str = "",
        namespace: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourcesFetched:
        """Get Resources list by namespace and kind"""
        try:
            resource_data = resource_store.get_many(
                namespace=namespace, kind=kind, category=category
            )
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

    @router.put("/resource")
    async def put_resource(
        resource_data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceUpdated:
        """Create or update a resource"""

        try:
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

    @router.delete(
        "/resource/{namespace}/{category}",
        description="Delete all resources by namespace and category",
    )
    @router.delete(
        "/resource/{namespace}/{kind}",
        description="Delete all resources by namespace and kind",
    )
    async def delete_resources(
        namespace: str = "",
        kind: str = "",
        name: str = "",
        category: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceDeleted:
        """Deletes a resource by namespace, kind and name."""

        try:
            resource_data = resource_store.delete_many(
                namespace=namespace, kind=kind, category=category, name=name
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

    @router.delete(
        "/resource/{namespace}/{kind}/{name}",
        description="Delete a resource by namespace, kind and name",
    )
    async def delete_resource(
        namespace: str = "",
        kind: str = "",
        name: str = "",
        category: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceDeleted:
        """Deletes a resource by namespace, kind and name."""

        try:
            resource_data = resource_store.delete(
                namespace=namespace, kind=kind, category=category, name=name
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

    return router
