"""Test configuration for pytest."""
import json
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from feature_store.server.database import DBFeature


@pytest_asyncio.fixture(autouse=True)
async def setup_db() -> None:
    """Setup the database."""
    client = AsyncMongoMockClient()
    await init_beanie(
        database=client.test_db,
        document_models=[DBFeature],  # type: ignore
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    """Adds the --e2e option to pytest."""
    parser.addoption("--e2e", action="store_true", default=False, help="run e2e tests")


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Modifies the collection of tests to skip e2e tests if --e2e is not specified."""
    if config.getoption("--e2e"):
        return
    skip_e2e = pytest.mark.skip(reason="need --e2e option to run")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)


@pytest.fixture(scope="session")
def geojson_features() -> dict[str, object] | Any:
    """Test fixture for geojson features."""
    test_feature_file = Path("test/data/test_features.json")
    with test_feature_file.open() as f:
        geojson = json.load(f)
    return geojson["features"]


@pytest.fixture(scope="session")
def geospatial_query_features() -> dict[str, object] | Any:
    """Test fixture for geojson features."""
    test_feature_file = Path("test/data/geospatial-search.json")
    with test_feature_file.open() as f:
        geojson = json.load(f)

    features = {}
    for feature in geojson["features"]:
        features[feature["properties"]["featureTest"]] = feature

    return features
