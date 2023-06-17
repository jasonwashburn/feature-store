"""Implements tests for the Feature Store API."""
from fastapi.testclient import TestClient

from feature_store.server.app import app

client = TestClient(app)


def test_read_root() -> None:
    """Tests the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Feature Store!"}
