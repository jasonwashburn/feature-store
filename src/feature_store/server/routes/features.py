"""Implementation of the features endpoint."""
from fastapi.routing import APIRouter

from feature_store.server.models.geojson import Feature

router = APIRouter()


@router.get("/")
async def read_features() -> dict[str, str]:
    """Returns a welcome message.

    Returns:
        dict: A welcome message.
    """
    return {"message": "This is the features endpoint!"}


@router.post("/")
async def post_features(feature: Feature) -> Feature:
    """Returns a welcome message.

    Returns:
        dict: A welcome message.
    """
    return feature
