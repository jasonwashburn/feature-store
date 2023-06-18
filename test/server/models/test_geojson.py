"""Implements tests for GeoJSON models."""
import json

import pytest
from pydantic import ValidationError

from feature_store.server.models.geojson import (
    Feature,
    FeatureCollection,
    GeoJSONType,
    Geometry,
    GeometryType,
)


@pytest.fixture(scope="session")
def polygon_feature() -> Feature:
    """Returns a polygon Feature for use in tests.

    Returns:
        Feature: A polygon Feature.
    """
    return Feature(
        geojson_type=GeoJSONType.FEATURE,
        geometry=Geometry(
            geometry_type=GeometryType.POLYGON,
            coordinates=[
                [
                    [-10.0, -10.0],
                    [10.0, -10.0],
                    [10.0, 10.0],
                    [-10.0, 10.0],
                    [-10.0, -10.0],
                ],
            ],
        ),
        properties={},
    )


def test_feature_collection_can_build(polygon_feature: Feature) -> None:
    """Tests FeatureCollection can be built."""
    assert (
        FeatureCollection(
            geojson_type=GeoJSONType.FEATURE_COLLECTION,
            features=[polygon_feature],
        )
        is not None
    )


def test_feature_collection_rejects_invalid_geojson_type(
    polygon_feature: Feature,
) -> None:
    """Tests FeatureCollection rejects invalid GeoJSON type."""
    with pytest.raises(ValidationError):
        FeatureCollection(
            geojson_type="InvalidGeoJSONType",  # type: ignore
            features=[polygon_feature],
        )


def test_feature_collection_outputs_valid_geojson(polygon_feature: Feature) -> None:
    """Tests FeatureCollection outputs valid GeoJSON."""
    expected = json.dumps(
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [
                                    -10.0,
                                    -10.0,
                                ],
                                [
                                    10.0,
                                    -10.0,
                                ],
                                [
                                    10.0,
                                    10.0,
                                ],
                                [
                                    -10.0,
                                    10.0,
                                ],
                                [
                                    -10.0,
                                    -10.0,
                                ],
                            ],
                        ],
                    },
                    "properties": {},
                },
            ],
        },
    )
    actual = FeatureCollection(
        geojson_type=GeoJSONType.FEATURE_COLLECTION,
        features=[polygon_feature],
    ).json(by_alias=True)

    assert actual == expected
