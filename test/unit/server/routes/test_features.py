"""Implements tests for the features endpoint."""

from fastapi.testclient import TestClient

from feature_store.server.app import app

client = TestClient(app)
FEATURES_ROUTE = "/features"


def test_get_features() -> None:
    """Tests the features endpoint."""
    result = client.get(FEATURES_ROUTE)
    assert result.status_code == 404
    assert result.json() == {"detail": "No features found!"}


def test_put_feature() -> None:
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
    result = client.post(FEATURES_ROUTE, json=feature)
    assert result.status_code == 200
    for key in feature:
        assert result.json()[key] == feature[key]
    assert result.json()["_id"] is not None


def test_put_then_delete_multiple_features(geojson_features: dict[str, object]) -> None:
    """Inserts multiple features, then deletes them."""
    inserted_feature_ids = []
    for feature in geojson_features:
        insert_result = client.post(FEATURES_ROUTE, json=feature)
        assert insert_result.status_code == 200
        assert insert_result.json()["_id"] is not None
        inserted_feature_ids.append(insert_result.json()["_id"])

    for feature_id in inserted_feature_ids:
        delete_result = client.delete(f"{FEATURES_ROUTE}/{feature_id}")
        assert delete_result.status_code == 200
        assert delete_result.json() == {"message": f"Feature id: {feature_id} deleted!"}


def test_post_then_update_feature(geojson_features: list[dict[str, object]]) -> None:
    """Inserts a feature, then updates it."""
    feature = geojson_features[0]
    insert_result = client.post(FEATURES_ROUTE, json=feature)
    assert insert_result.status_code == 200
    assert insert_result.json()["_id"] is not None
    feature_id = insert_result.json()["_id"]

    new_feature = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "coordinates": [
                [
                    -1,
                    1,
                ],
                [
                    -2,
                    2,
                ],
                [
                    -3,
                    3,
                ],
            ],
            "type": "LineString",
        },
    }
    update_result = client.put(f"{FEATURES_ROUTE}/{feature_id}", json=new_feature)
    assert update_result.status_code == 200
    for key in new_feature:
        assert update_result.json()[key] == new_feature[key]
    assert update_result.json()["_id"] is not None
    assert update_result.json()["_id"] == feature_id
