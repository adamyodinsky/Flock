# coding: utf-8

from fastapi.testclient import TestClient

from server.schemas.internal_server_error import InternalServerError1  # noqa: F401
from server.schemas.resource_accepted import ResourceAccepted  # noqa: F401
from server.schemas.resource_bad_request import ResourceBadRequest1  # noqa: F401
from server.schemas.resource_created import ResourceCreated  # noqa: F401
from server.schemas.resource_data import ResourceData  # noqa: F401
from server.schemas.resource_not_found import ResourceNotFound1  # noqa: F401
from server.schemas.resource_updated import ResourceUpdated  # noqa: F401
from server.schemas.resources_fetched import ResourcesFetched  # noqa: F401
from server.schemas.responses.resource_already_exists import (
    ResourceAlreadyExists1,
)  # noqa: F401
from server.schemas.responses.resource_deleted import ResourceDeleted  # noqa: F401


def test_delete_resource_namespace_kind(client: TestClient):
    """Test case for delete_resource_namespace_kind

    delete-resource-namespace-kind
    """

    headers = {}
    response = client.request(
        "DELETE",
        "/resource/{namespace}/{kind}".format(
            namespace="namespace_example", kind="kind_example"
        ),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_delete_resource_namespace_kind_name(client: TestClient):
    """Test case for delete_resource_namespace_kind_name

    delete-resource-namespace-kind-name
    """

    headers = {}
    response = client.request(
        "DELETE",
        "/resource/{namespace}/{kind}/{name}".format(
            namespace="namespace_example", kind="kind_example", name="name_example"
        ),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_resource(client: TestClient):
    """Test case for post_resource

    post-resource
    """
    resource_data = null

    headers = {}
    response = client.request(
        "POST",
        "/resource/{namespace}/{kind}/{name}".format(
            namespace="namespace_example", kind="kind_example", name="name_example"
        ),
        headers=headers,
        json=resource_data,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_put_resource(client: TestClient):
    """Test case for put_resource

    put-resource
    """
    resource_data = null

    headers = {}
    response = client.request(
        "PUT",
        "/resource/{namespace}/{kind}/{name}".format(
            namespace="namespace_example", kind="kind_example", name="name_example"
        ),
        headers=headers,
        json=resource_data,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
