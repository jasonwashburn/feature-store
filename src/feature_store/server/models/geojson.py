"""Implements Pydantic models to store GeoJSON data."""
from enum import Enum

from pydantic import BaseModel, Field


class GeoJSONType(str, Enum):
    """Represents valid GeoJSON types."""

    FEATURE_COLLECTION = "FeatureCollection"
    FEATURE = "Feature"


class GeometryType(str, Enum):
    """Represents valid GeoJSON geometry types."""

    POINT = "Point"
    LINE_STRING = "LineString"
    POLYGON = "Polygon"


class Geometry(BaseModel):
    """Implements a Geometry model."""

    geometry_type: GeometryType
    coordinates: list[list[list[float]]]

    class Config:
        """Configures the Geometry model."""

        fields = {"geometry_type": "type"}
        allow_population_by_field_name = True


class Feature(BaseModel):
    """Implements a Feature model."""

    geojson_type: GeoJSONType = Field(default=GeoJSONType.FEATURE)
    geometry: Geometry
    properties: dict[str, str]

    class Config:
        """Configures the Feature model."""

        fields = {"geojson_type": "type"}

        allow_population_by_field_name = True


class FeatureCollection(BaseModel):
    """Implements a Feature Collection model."""

    geojson_type: GeoJSONType = Field(default=GeoJSONType.FEATURE_COLLECTION)
    features: list[Feature]

    class Config:
        """Configures the Feature Collection model."""

        fields = {"geojson_type": "type"}
        allow_population_by_field_name = True
