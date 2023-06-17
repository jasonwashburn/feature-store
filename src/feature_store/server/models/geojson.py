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

    def to_dict(self) -> dict[str, list[list[list[float]]] | str]:
        """Converts the Geometry to a dictionary."""
        return {
            "type": self.geometry_type.value,
            "coordinates": self.coordinates,
        }


class Feature(BaseModel):
    """Implements a Feature model."""

    geojson_type: GeoJSONType = Field(default=GeoJSONType.FEATURE)
    geometry: Geometry
    properties: dict[str, str]

    def to_dict(
        self,
    ) -> dict[str, object]:
        """Converts the Feature to a dictionary."""
        return {
            "type": self.geojson_type.value,
            "geometry": self.geometry.to_dict(),
            "properties": self.properties,
        }


class FeatureCollection(BaseModel):
    """Implements a Feature Collection model."""

    geojson_type: GeoJSONType = Field(default=GeoJSONType.FEATURE_COLLECTION)
    features: list[Feature]

    def to_dict(self) -> dict[str, object]:
        """Converts the FeatureCollection to a dictionary."""
        return {
            "type": self.geojson_type.value,
            "features": [feature.to_dict() for feature in self.features],
        }
