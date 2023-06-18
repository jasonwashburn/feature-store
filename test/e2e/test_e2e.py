"""Implements end-to-end tests for the API."""
import json
from pathlib import Path

import httpx
import pytest

HOST = "http://localhost:8000"
TEST_FILE_PATH = "test/data/geojson-test.json"


@pytest.mark.e2e()
@pytest.mark.timeout(10)
def test_features_is_empty() -> None:
    """Tests the features endpoint."""
    with httpx.Client(base_url=HOST) as client:
        result = client.get("/features/")
        assert result.status_code == 404
        assert result.json() == {"detail": "No features found!"}


@pytest.mark.e2e()
@pytest.mark.timeout(5)
def test_post_multiple_geojson_features() -> None:
    """Tests you can post multiple geojson features to features endpoint."""
    geojson_file = Path(TEST_FILE_PATH)
    with geojson_file.open("r") as file:
        geojson = json.load(file)

    inserted_ids = []
    with httpx.Client(base_url=HOST) as client:
        for feature in geojson["features"]:
            result = client.post("/features/", json=feature)
            assert result.status_code == 200
            for sent_key, sent_value in feature.items():
                assert result.json()[sent_key] == sent_value
            assert result.json()["_id"] is not None
            inserted_ids.append(result.json()["_id"])
