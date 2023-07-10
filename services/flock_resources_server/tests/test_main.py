"""Test the API endpoints using FastAPI's TestClient."""

import os

import pytest
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from flock_common import check_env_vars
from flock_resource_store import ResourceStoreFactory
from flock_schema_store import SchemaStoreFactory
from flock_schemas import SchemaFactory

from flock_resources_server.api.resource_api import ResourceBuilder, get_router

app = FastAPI()

load_dotenv(find_dotenv(os.environ.get("FLOCK_ENV_FILE", ".env")))
check_env_vars([], [])

resource_store = ResourceStoreFactory.get_resource_store("mongo")
resource_builder = ResourceBuilder(resource_store)
schema_store = SchemaStoreFactory.get_store("mongo")
schema_factory = SchemaFactory()

router = get_router(resource_store, resource_builder, schema_store, "resources-server")
app.include_router(router)

client = TestClient(app)


@pytest.fixture
def test_data():
    """Test data"""
    return [
        schema_factory.get_schema(kind="Splitter")
        .validate(
            {
                "apiVersion": "flock/v1",
                "kind": "Splitter",
                "namespace": "bla",
                "category": "other",
                "created_at": None,
                "updated_at": None,
                "metadata": {
                    "name": "test-1",
                    "description": "text-splitter",
                    "annotations": {},
                    "labels": {"app": "my_app"},
                },
                "spec": {
                    "vendor": "CharacterTextSplitter",
                    "options": {"chunk_size": 30, "chunk_overlap": 0},
                },
            }
        )
        .dict(),
        schema_factory.get_schema(kind="Splitter")
        .validate(
            {
                "apiVersion": "flock/v1",
                "kind": "Splitter",
                "namespace": "bla",
                "category": "other",
                "created_at": None,
                "updated_at": None,
                "metadata": {
                    "name": "test-2",
                    "description": "text-splitter",
                    "annotations": {},
                    "labels": {"app": "my_app"},
                },
                "spec": {
                    "vendor": "CharacterTextSplitter",
                    "options": {"chunk_size": 30, "chunk_overlap": 0},
                },
            }
        )
        .dict(),
    ]


@pytest.fixture(autouse=True)
def setup_and_cleanup(test_data):
    # Setup - insert test data into resource_store
    for data in test_data:
        resource_store.put(data)

    yield  # This is where the test function gets run

    resource_store.delete_many(
        namespace=test_data[0]["namespace"], kind=test_data[0]["kind"]
    )


def test_get_resource(test_data):
    """Test get_resource endpoint"""

    response = client.get(
        f"/resource/?namespace={test_data[0]['namespace']}&kind={test_data[0]['kind']}&name={test_data[0]['metadata']['name']}"
    )

    response_body = response.json()["data"]

    assert response.status_code == 200
    assert response_body["id"] is not None

    test_data[0]["id"] = response_body["id"]
    assert response_body == test_data[0]

    response = client.get(f"/resource/?id={test_data[0]['id']}")


def test_get_resources(test_data):
    """Test get_resources endpoint"""

    response = client.get(
        f"/resources/?namespace={test_data[0]['namespace']}&kind={test_data[0]['kind']}"
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_post_resource(test_data):
    """Test put_resource endpoint"""

    resource_store.delete_many(
        namespace=test_data[0]["namespace"], kind=test_data[0]["kind"]
    )

    resource_data = test_data[0]
    response = client.post("/resource", json=resource_data)
    assert response.status_code == 200

    # Check if the resource is created
    response = client.get(
        f"/resource/?namespace={resource_data['namespace']}&kind={resource_data['kind']}&name={resource_data['metadata']['name']}"
    )
    response_body = response.json()["data"]

    assert response.status_code == 200
    assert response_body["id"] is not None

    resource_data["id"] = response_body["id"]
    assert response_body == resource_data


def test_put_resource(test_data):
    """Test put_resource endpoint"""

    resource_data = test_data[0]
    response = client.put(f"/resource/{resource_data['id']}", json=resource_data)
    assert response.status_code == 200

    # Check if the resource is created
    response = client.get(
        f"/resource/?namespace={resource_data['namespace']}&kind={resource_data['kind']}&name={resource_data['metadata']['name']}"
    )
    response_body = response.json()["data"]

    assert response.status_code == 200
    assert response_body["id"] is not None

    resource_data["id"] = response_body["id"]
    assert response_body == resource_data


def test_delete_resource(test_data):
    """Test delete_resource endpoint"""

    response = client.delete(
        f"/resource/?namespace={test_data[0]['namespace']}&kind={test_data[0]['kind']}&name={test_data[0]['metadata']['name']}"
    )
    assert response.status_code == 200

    # Check if the resource is deleted
    response = client.get(
        f"/resource/?namespace={test_data[0]['namespace']}&kind={test_data[0]['kind']}&name={test_data[0]['metadata']['name']}"
    )
    assert response.status_code == 404

    response = client.get(
        f"/resource/?namespace={test_data[1]['namespace']}&kind={test_data[1]['kind']}&name={test_data[1]['metadata']['name']}"
    )
    assert response.status_code == 200


def test_delete_resources(test_data):
    """Test delete_resources endpoint"""

    response = client.delete(
        f"/resource/?namespace={test_data[0]['namespace']}&kind={test_data[0]['kind']}"
    )
    assert response.status_code == 200

    # Check if the resources are deleted
    response = client.get(
        f"/resource/?namespace={test_data[0]['namespace']}&kind={test_data[0]['kind']}&name={test_data[0]['metadata']['name']}"
    )
    assert response.status_code == 404
    response = client.get(
        f"/resource/?namespace={test_data[1]['namespace']}&kind={test_data[1]['kind']}&name={test_data[1]['metadata']['name']}"
    )
    assert response.status_code == 404


def test_get_schema():
    """Test delete_resources endpoint"""

    response = client.get("/schema/Agent")
    assert response.status_code == 200
    assert response.json()["data"] is not None


def test_get_schemas():
    """Test delete_resources endpoint"""

    response = client.get("/schemas")
    assert response.status_code == 200
    assert response.json()["data"] is not None


def test_get_kinds():
    """Test delete_resources endpoint"""

    response = client.get("/kinds")
    assert response.status_code == 200
    assert response.json()["data"] is not None


if __name__ == "__main__":
    pytest.main()
