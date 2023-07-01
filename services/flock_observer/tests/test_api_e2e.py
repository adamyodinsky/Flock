"""End-to-end tests for the API."""

import os

import httpx
import pytest

BASE_URL = os.environ.get("BASE_URL", "http://localhost:9001")


def test_health_endpoint():
    response = httpx.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_endpoint():
    response = httpx.get(f"{BASE_URL}/metrics/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_details_endpoint():
    response = httpx.get(f"{BASE_URL}/details/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_logs_endpoint():
    response = httpx.get(f"{BASE_URL}/logs/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
