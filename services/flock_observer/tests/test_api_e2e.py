"""End-to-end tests for the API."""

import os

import httpx
import pytest

BASE_URL = os.environ.get(
    "BASE_URL", f"http://localhost:{os.environ.get('PORT', '9001')}"
)
NAMESPACE = "default"
DEPLOYMENT = "my-agent"
KIND = "FlockDeployment"


def test_health_endpoint():
    response = httpx.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_metrics_endpoint():
    response = httpx.get(f"{BASE_URL}/metrics")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(f"{BASE_URL}/metrics?kind={KIND}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(f"{BASE_URL}/metrics?kind={KIND}&namespace={NAMESPACE}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(
        f"{BASE_URL}/metrics?kind={KIND}&namespace={NAMESPACE}&name={DEPLOYMENT}"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_details_endpoint():
    response = httpx.get(f"{BASE_URL}/details")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(f"{BASE_URL}/details?kind={KIND}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(f"{BASE_URL}/details?kind={KIND}&namespace={NAMESPACE}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(
        f"{BASE_URL}/details?kind={KIND}&namespace={NAMESPACE}&name={DEPLOYMENT}"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_logs_endpoint():
    response = httpx.get(f"{BASE_URL}/logs")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(f"{BASE_URL}/logs?kind={KIND}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(f"{BASE_URL}/logs?kind={KIND}&namespace={NAMESPACE}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = httpx.get(
        f"{BASE_URL}/logs?kind={KIND}&namespace={NAMESPACE}&name={DEPLOYMENT}"
    )
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main(["-v", __file__])
