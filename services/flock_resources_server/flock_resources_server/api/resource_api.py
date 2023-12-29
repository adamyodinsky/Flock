"""Flock API"""

from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from flock_builder import ResourceBuilder
from flock_resource_store.mongo import ResourceStore
from flock_schema_store import SchemaStore
from flock_schemas import BaseResourceSchema, SchemaFactory
from pydantic import ValidationError

from flock_resources_server.schemas.resource_details import ResourceDetails
from flock_resources_server.schemas.responses.resource_fetched import ListData
from flock_resources_server.schemas.status_code import ResourceType


def get_router(
    resource_store: ResourceStore,
    resource_builder: ResourceBuilder,
    schema_store: SchemaStore,
    prefix: str,
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
        schema_store: SchemaStore = Depends(lambda: schema_store),
    ):
        """Health check"""

        resource_store_health = resource_store.health_check()
        schema_store_health = schema_store.health_check()

        if resource_store_health and schema_store_health:
            return {
                "status": "OK",
                "resource_store": resource_store_health,
                "schema_store": schema_store_health,
            }
        raise HTTPException(
            status_code=500,
            detail=[
                "Resource store is not healthy",
            ],
        )

    @router.get("/resource")
    @router.get("/resource/{id}")
    async def get_resource(
        namespace: str = "",
        kind: str = "",
        category: str = "",
        name: str = "",
        id: str = "",
        tool: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> dict:
        """Get a resource"""
        try:
            resource_data = resource_store.get(
                namespace=namespace,
                kind=kind,
                category=category,
                name=name,
                id=id,
                tool=tool,
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

            return resource_data

        except HTTPException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
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
        tool: str = "",
        page: int = 1,
        page_size: int = 50,
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> ListData:
        """Get Resources list by namespace and kind"""
        # res.headers["Access-Control-Allow-Origin"] = "*"
        try:
            resource_data = resource_store.get_many(
                namespace=namespace,
                kind=kind,
                category=category,
                tool=tool,
                page=page,
                page_size=page_size,
            )

            total_count = resource_store.total(
                namespace=namespace,
                kind=kind,
                category=category,
                tool=tool,
            )

            fetched_resources = [
                ResourceDetails.validate(item) for item in resource_data
            ]
            return ListData(
                items=fetched_resources,
                count=len(fetched_resources),
                total=total_count,
            )

        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to get resource",
                    f"namespace: {namespace}",
                    f"kind: {kind}",
                    f"category: {category}",
                    str(error),
                ],
            ) from error

    @router.post("/resource")
    async def create_resource(
        resource_data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceType:
        """Create or update a resource.

        If the resource already exists, an error will be returned.
        """

        try:
            name: str = resource_data["metadata"]["name"]
            namespace: str = resource_data["namespace"]
            kind: str = resource_data["kind"]
        except KeyError as error:
            raise HTTPException(
                status_code=422,
                detail=["Failed to build resource", str(error)],
            ) from error

        if resource_store.get(namespace=namespace, kind=kind, name=name) is not None:
            raise HTTPException(
                status_code=422,
                detail=[
                    "Resource already exists",
                    f"namespace: {namespace}",
                    f"kind: {kind}",
                    f"name: {name}",
                ],
            )

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
                status_code=400,
                detail=["Failed to build resource", str(error)],
            ) from error

        # store resource
        try:
            resource_store.put(val=schema_instance.dict(by_alias=True))
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return schema_instance

    @router.put("/resource/{id}")
    async def put_resource(
        resource_data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
        id: str = "",
    ) -> ResourceType:
        """Create or update a resource.

        If the resource already exists, it will be updated. Otherwise, an error will be returned.
        """
        fetched_resource = {}
        try:
            fetched_resource = resource_store.get(id=id)
            if fetched_resource is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Resource not found",
                        f"id: {id}",
                    ],
                )
        except HTTPException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to fetch resource",
                    str(error),
                ],
            ) from error

        resource_data["id"] = fetched_resource["id"]

        try:
            schema_instance = schema_factory.get_schema(resource_data["kind"]).validate(
                resource_data
            )
            resource_builder.build_resource(resource_data)
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=["Failed to build resource", str(error)],
            ) from error

        # store resource
        try:
            resource_store.put(val=schema_instance.dict(by_alias=True))
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to store resource",
                    str(error),
                ],
            ) from error

        return schema_instance

    @router.delete(
        "/resource",
        description="Delete resource",
    )
    @router.delete(
        "/resource/{id}",
        description="Delete resource",
    )
    async def delete_resource(
        namespace: str = "",
        kind: str = "",
        category: str = "",
        name: str = "",
        id: str = "",
        tool: str = "",
        resource_store: ResourceStore = Depends(lambda: resource_store),
    ) -> List[str]:
        """Deletes a resource."""

        try:
            resource_data = resource_store.delete_many(
                namespace=namespace,
                kind=kind,
                category=category,
                name=name,
                id=id,
                tool=tool,
            )
            return [
                "Resource deleted",
                f"Parameters: namespace={namespace}, kind={kind}, category={category}, name={name}, id={id}",
                f"Count: {resource_data.deleted_count}",  # type: ignore
            ]

        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to delete resource",
                    str(error),
                ],
            ) from error

    @router.post("/resource/validate")
    async def validate_resource(
        resource_data: dict = Body(..., description=""),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceType:
        """Resource validation only

        This endpoint does not store the resource. It is used to validate the resource only.
        """

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

        return schema_instance

    @router.get("/schema/{kind}")
    async def get_schema(
        schema_store: SchemaStore = Depends(lambda: schema_store), kind: str = ""
    ) -> dict:
        """Get schema for kind"""
        try:
            schema_data = schema_store.get(kind=kind)

            if schema_data is None:
                raise HTTPException(
                    status_code=404,
                    detail=[
                        "Schema not found",
                        f"kind: {kind}",
                    ],
                )

            return schema_data

        except HTTPException as error:
            raise error
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to get schema",
                    str(error),
                ],
            ) from error

    @router.get("/schemas")
    async def get_schemas(
        schema_store: SchemaStore = Depends(lambda: schema_store),
    ) -> ListData:
        """Get all schemas"""

        try:
            schemas_data = schema_store.get_many()
            total = schema_store.total()

            return ListData(items=schemas_data, count=len(schemas_data), total=total)

        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=[
                    "Failed to get schemas",
                    str(error),
                ],
            ) from error

    @router.get("/kinds")
    async def get_kinds(
        schema_store: SchemaStore = Depends(lambda: schema_store),
    ) -> ListData:
        """Get all kinds"""
        try:
            kinds_data = schema_store.get_kinds()
            total = len(kinds_data)

            return ListData(items=kinds_data, count=len(kinds_data), total=total)

        except Exception as error:
            raise HTTPException(
                status_code=500,
                detail=[
                    "Failed to get kinds",
                    str(error),
                ],
            ) from error

    @router.post("/shortcut")
    async def create_vector_store(
        data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ) -> ResourceType:
        """Create vector store"""

        dependencies = []

        try:
            kind = data["kind"]
            name: str = data["name"]
            namespace: str = data["namespace"]
            description: str = data["description"]
            dependencies_ids: list[str] = data["dependency_ids"]
        except KeyError as error:
            raise HTTPException(
                status_code=400,
                detail=[
                    "Invalid request",
                    str(error),
                ],
            ) from error

        for dependency_id in dependencies_ids:
            dependency_resource = resource_store.get(id=dependency_id)
            if not resource_store.get(id=dependency_id):
                raise HTTPException(
                    status_code=422,
                    detail=[
                        "Dependency does not exist",
                        f"id: {dependency_id}",
                    ],
                )
            dependencies.append(dependency_resource)

        if resource_store.get(namespace=namespace, kind=kind, name=name) is not None:
            raise HTTPException(
                status_code=422,
                detail=[
                    "Resource already exists",
                    f"namespace: {namespace}",
                    f"kind: {kind}",
                    f"name: {name}",
                ],
            )

        # create vector store resource

        vectorstore_schema_cls = schema_factory.get_schema(kind).validate(data)
        vectorstore_dict = {
            "apiVersion": "flock/v1",
            "kind": kind,
            "namespace": namespace,
            "metadata": {"name": name, "description": description},
            "spec": {
                "vendor": "Chroma",
                "dependencies": [
                    {
                        "name": dependency.get("metadata", {}).get("name"),
                        "namespace": dependency.get("namespace"),
                        "kind": dependency.get("kind"),
                    }
                    for dependency in dependencies
                ],
            },
        }

        try:
            schema_instance = vectorstore_schema_cls.validate(**vectorstore_dict)
            resource_builder.build_resource(schema_instance.dict())
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=["Failed to build resource", str(error)],
            ) from error

        return schema_instance

    # shortcut/webscraper job, with the vector store id.
    @router.post("/shortcut/WebsScraper")
    async def create_webscraper(
        data: dict = Body(..., description=""),
        resource_store: ResourceStore = Depends(lambda: resource_store),
        schema_factory: SchemaFactory = Depends(lambda: schema_factory),
    ):
        webscraper_kind = "WebScraper"
        vector_store_id = data["vector_store_id"]
        namespace: str = data["namespace"]
        name: str = data["name"]
        description: str = data["description"]

        # check if vector store exists
        vector_store = resource_store.get(id=vector_store_id)
        if vector_store is None:
            raise HTTPException(
                status_code=422,
                detail=[
                    "Vector store does not exist",
                    f"id: {vector_store_id}",
                ],
            )

        # create webscraper resource
        webscraper_dict = {
            "apiVersion": "flock/v1",
            "kind": webscraper_kind,
            "namespace": namespace,
            "metadata": {"name": name, "description": description},
            "spec": {
                "dependencies": [
                    {
                        "name": vector_store.get("metadata", {}).get("name"),
                        "namespace": vector_store.get("namespace"),
                        "kind": vector_store.get("kind"),
                    }
                ],
            },
        }

        try:
            webscraper_schema_cls = schema_factory.get_schema(webscraper_kind).validate(
                webscraper_dict
            )
            schema_instance = webscraper_schema_cls.validate(**webscraper_dict)
            resource_builder.build_resource(schema_instance.dict())
        except Exception as error:  # pylint: disable=broad-except
            raise HTTPException(
                status_code=500,
                detail=["Failed to build resource", str(error)],
            ) from error

    return router
