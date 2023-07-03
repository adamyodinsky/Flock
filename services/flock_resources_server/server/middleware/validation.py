import time

from fastapi import FastAPI, Request
from flock_models.builder import ResourceBuilder
from flock_schemas import SchemasFactory

app = FastAPI()


@app.middleware("http")
async def validate(request: Request, call_next):
    """Validate resource data before storing it."""

    # try:
    #     assert namespace == resource_data["namespace"]
    #     assert kind == resource_data["kind"]
    #     assert name == resource_data["metadata"]["name"]
    # except AssertionError:
    #     return ResourceBadRequest(
    #         details=[
    #             "Resource data does not match parameters",
    #             f"Parameters: {namespace}/{kind}/{name}",
    #             f"Schema: {resource_data['namespace']}/{resource_data['kind']}/{resource_data['metadata']['name']}",
    #         ],
    #     )

    # try:
    #     # validate resource building
    #     resource_builder.build_resource(resource_data)
    # except ValidationError as error:
    #     return ResourceBadRequest(
    #         details=["Failed to build resource", str(error)],
    #     )
    # except Exception as error:  # pylint: disable=broad-except
    #     return InternalServerError(
    #         details=["Failed to build resource", str(error)],
    #     )

    # # store resource
    # try:
    #     resource_store.put(
    #         key=f"{namespace}/{kind}/{name}",
    #         val=resource_data,
    #     )
    # except Exception as error:  # pylint: disable=broad-except
    #     return InternalServerError(
    #         details=[
    #             "Failed to store resource",
    #             str(error),
    #         ],
    #     )
    print("middleware")
    response = await call_next(request)

    return response
