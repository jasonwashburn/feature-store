"""Implements end-to-end tests for the API."""
import json
from pathlib import Path

import httpx
import pytest

HOST = "http://localhost:8000"
TEST_FILE_PATH = "test/data/geojson-test.json"
FEATURES_ROUTE = "/features/"

inserted_ids = []


@pytest.mark.e2e()
@pytest.mark.timeout(10)
def test_features_is_empty() -> None:
    """Tests the features endpoint."""
    with httpx.Client(base_url=HOST) as client:
        result = client.get(FEATURES_ROUTE)
        assert result.status_code == 404
        assert result.json() == {"detail": "No features found!"}


@pytest.mark.e2e()
@pytest.mark.timeout(5)
def test_post_multiple_geojson_features() -> None:
    """Tests you can post multiple geojson features to features endpoint."""
    geojson_file = Path(TEST_FILE_PATH)
    with geojson_file.open("r") as file:
        geojson = json.load(file)

    with httpx.Client(base_url=HOST) as client:
        for feature in geojson["features"]:
            result = client.post(FEATURES_ROUTE, json=feature)
            assert result.status_code == 200
            for sent_key, sent_value in feature.items():
                assert result.json()[sent_key] == sent_value
            assert result.json()["_id"] is not None
            inserted_ids.append(result.json()["_id"])


@pytest.mark.e2e()
@pytest.mark.timeout(5)
def test_put_feature() -> None:
    """Tests you can update a feature."""
    feature_id = inserted_ids[0]

    with httpx.Client(base_url=HOST) as client:
        update = {"properties": {"name": "Updated Feature"}}
        result = client.put(f"{FEATURES_ROUTE}{feature_id}", json=update)
        assert result.status_code == 200
        assert result.json()["properties"]["name"] == "Updated Feature"


@pytest.mark.e2e()
@pytest.mark.timeout(5)
def test_get_geo_intersects(
    geospatial_query_features: dict[str, str | dict[str, object]],
) -> None:
    """Tests you can query for features that intersect a polygon."""
    geospatial_test_feature_ids = []
    with httpx.Client(base_url=HOST) as client:
        for key in ["point", "line", "box"]:
            feature = geospatial_query_features.get(key)
            insert_result = client.post(FEATURES_ROUTE, json=feature)
            assert insert_result.status_code == 200
            assert insert_result.json()["_id"] is not None
            inserted_ids.append(insert_result.json()["_id"])
            geospatial_test_feature_ids.append(insert_result.json()["_id"])

    polygon = geospatial_query_features.get("outer-box").get("geometry")  # type: ignore

    with httpx.Client(base_url=HOST) as client:
        result = client.post(
            f"{FEATURES_ROUTE}geospatial/intersects",
            json=polygon,
        )
        assert result.status_code == 200
        assert len(result.json()) == 3
        assert all(
            feature["_id"] in geospatial_test_feature_ids for feature in result.json()
        )


@pytest.mark.e2e()
@pytest.mark.timeout(5)
def test_delete_inserted_features() -> None:
    """Tests you can delete the inserted features."""
    with httpx.Client(base_url=HOST) as client:
        for feature_id in inserted_ids:
            result = client.delete(f"{FEATURES_ROUTE}{feature_id}")
            assert result.status_code == 200
            assert result.json() == {"message": f"Feature id: {feature_id} deleted!"}


@pytest.mark.e2e()
@pytest.mark.timeout(5)
def test_verify_no_features_remain() -> None:
    """Tests to ensure no unexpected features remain in the database."""
    with httpx.Client(base_url=HOST) as client:
        result = client.get(FEATURES_ROUTE)
        assert result.status_code == 404
        assert result.json() == {"detail": "No features found!"}
