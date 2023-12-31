"""Implements the database logic for the Feature Store server."""

import os

import pymongo
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from feature_store.server.models.geojson import (
    GeoJsonLineString,
    GeoJsonPoint,
    GeoJsonPolygon,
    GeoJSONType,
)

mongo_username = os.getenv("MONGODB_USERNAME")
mongo_password = os.getenv("MONGODB_PASSWORD")
mongo_host = os.getenv("MONGODB_HOST")
mongo_port = os.getenv("MONGODB_PORT")


class DBFeature(Document):
    """Implements a Feature model."""

    geojson_type: GeoJSONType
    geometry: GeoJsonPoint | GeoJsonPolygon | GeoJsonLineString
    properties: dict[str, str]

    class Config:
        """Configures the Feature model."""

        fields = {"geojson_type": "type"}

        allow_population_by_field_name = True

    class Settings:
        """Configures the database settings."""

        name = "features"
        indexes = [
            [("geometry", pymongo.GEOSPHERE)],
        ]


class UpdateDBFeature(BaseModel):
    """Implements a Feature model."""

    geojson_type: GeoJSONType | None
    geometry: GeoJsonPoint | GeoJsonPolygon | GeoJsonLineString | None
    properties: dict[str, str] | None

    class Config:
        """Configures the Feature model."""

        fields = {"geojson_type": "type"}
        allow_population_by_field_name = True


async def init_db() -> None:
    """Initializes the database."""
    client = AsyncIOMotorClient(
        f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}",
    )

    await init_beanie(
        database=client.feature_store,
        document_models=[DBFeature],  # type: ignore  # noqa: PGH003
    )
