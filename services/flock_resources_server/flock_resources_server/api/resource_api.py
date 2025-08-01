"""Flock API"""

import os

from fastapi import APIRouter, Body, Depends, HTTPException
from flock_builder import ResourceBuilder
from flock_resource_store.mongo import ResourceStore
from flock_schemas import SchemaFactory
from pydantic import ValidationError

from flock_resources_server.schemas.resource_details import ResourceDetails
from flock_resources_server.schemas.responses.resource_deleted import ResourceDeleted
from flock_resources_server.schemas.responses.resource_fetched import ResourceFetched
from flock_resources_server.schemas.responses.resource_updated import ResourceUpdated
from flock_resources_server.schemas.responses.resources_fetched import ResourcesFetched


def get_router(
    resource_store: ResourceStore, resource_builder: ResourceBuilder, prefix: str
) -> APIRouter:
    """Get API router"""

    router = APIRouter()
    schema_factory = SchemaFactory()

    @router.get("/")
    @router.get("/health")
    @router.head("/health")
    @router.get(f"/{prefix}/health")
    async def health(
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ):
        """Health check"""

        healthy = resource_store.health_check()

        if healthy:
            return {"status": "OK"}
        raise HTTPException(
            status_code=500,
            detail=[
                "Resource store is not healthy",
            ],
        )

    @router.get("/resource")
    async def get_resource(
        namespace: str = "",
        kind: str = "",
        category: str = "",
        name: str = "",
        page: int = 1,
        page_size: int = 50,
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceFetched:
        """Get a resource"""
        try:
            resource_data = resource_store.get(
                namespace=namespace, kind=kind, category=category, name=name
            )

            if resource_data is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Resource not found",
                        f"namespace: {namespace}",
                        f"kind: {kind}",
                        f"category: {category}",
                        f"name: {name}",
                    ],
                )

            return ResourceFetched(data=resource_data)

        except HTTPException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get resource",
                    str(error),
                ],
            ) from error

    @router.get("/resources")
    async def get_resources(
        kind: str = "",
        category: str = "",
        namespace: str = "",
        page: int = 1,
        page_size: int = 50,
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourcesFetched:
        """Get Resources list by namespace and kind"""
        try:
            resource_data = resource_store.get_many(
                namespace=namespace,
                kind=kind,
                category=category,
                page=page,
                page_size=page_size,
            )

            fetched_resources = [
                ResourceDetails.validate(item) for item in resource_data
            ]
            return ResourcesFetched(data=fetched_resources)

        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get resource",
                    f"namespace: {namespace}",
                    f"kind: {kind}",
                    f"category: {category}",
                    str(error),
                ],
            ) from error

    @router.put("/resource")
    async def put_resource(
        resource_data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceUpdated:
        """Create or update a resource"""

        try:
            schema_instance = schema_factory.get_schema(resource_data["kind"]).validate(
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
        "/resource",
        description="Delete resource",
    )
    async def delete_resource(
        namespace: str = "",
        kind: str = "",
        category: str = "",
        name: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ResourceDeleted:
        """Deletes a resource."""

        try:
            resource_data = resource_store.delete_many(
                namespace=namespace, kind=kind, category=category, name=name
            )
            return ResourceDeleted(
                details=[
                    "Resource deleted",
                    f"Parameters: namespace={namespace}, kind={kind}, category={category}, name={name}",
                    f"Count: {resource_data.deleted_count}",  # type: ignore
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

    @router.post("/resource/validate")
    async def validate_resource(
        resource_data: dict = Body(..., description=""),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceUpdated:
        """Create or update a resource"""

        try:
            schema_instance = schema_factory.get_schema(resource_data["kind"]).validate(
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

        return ResourceUpdated(data=schema_instance)

    return router
