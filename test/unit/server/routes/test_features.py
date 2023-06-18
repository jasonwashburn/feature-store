"""Implements tests for the features endpoint."""
from fastapi.testclient import TestClient

from feature_store.server.app import app

client = TestClient(app)


def test_get_features() -> None:
    """Tests the features endpoint."""
    result = client.get("/features")
    assert result.status_code == 404
    assert result.json() == {"detail": "No features found!"}


def test_put_features() -> None:
    """Tests the features endpoint."""
    feature = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "coordinates": [
                [
                    -9.043896765999108,
                    18.080726541014158,
                ],
                [
                    -15.094104441552815,
                    14.225375733286057,
                ],
                [
                    -7.644992354384158,
                    16.415190283123252,
                ],
            ],
            "type": "LineString",
        },
    }
    result = client.post("/features", json=feature)
    assert result.status_code == 200
    for key in feature:
        assert result.json()[key] == feature[key]
    assert result.json()["_id"] is not None
