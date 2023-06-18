"""Implementation of the features endpoint."""
from beanie import PydanticObjectId
from fastapi import HTTPException
from fastapi.routing import APIRouter

from feature_store.server.database import DBFeature

router = APIRouter()


@router.post("/")
async def post_features(feature: DBFeature) -> DBFeature:
    """Returns a welcome message.

    Returns:
        dict: A welcome message.
    """
    return await feature.create()


@router.get("/")
async def get_features() -> list[DBFeature]:
    """Returns all features in the database.

    Raises:
        HTTPException: If no features are found.

    Returns:
        list[DBFeature]: A list of features.
    """
    result = await DBFeature.find_all().to_list()
    if not isinstance(result, list) or len(result) == 0:
        raise HTTPException(
            status_code=404,
            detail="No features found!",
        )

    return result


@router.get("/{feature_id}", response_description="Review record retrieved")
async def get_feature_by_id(feature_id: PydanticObjectId) -> DBFeature:
    """Returns a feature by id.

    Args:
        feature_id (PydanticObjectId): The id of the feature to return.

    Raises:
        HTTPException: If the feature is not found.

    Returns:
        DBFeature: The feature.
    """
    result = await DBFeature.get(feature_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Feture id: {feature_id} not found!",
        )
    return result


@router.delete(
    "/{feature_id}",
    response_description="Feature deleted from the database",
)
async def delete_feature_by_id(feature_id: PydanticObjectId) -> dict[str, str]:
    """Deletes a feature by id.

    Args:
        feature_id (PydanticObjectId): The id of the feature to delete.


    Raises:
        HTTPException: If the feature is not found.
        HTTPException: If the feature is not deleted.

    Returns:
        dict[str, str]: A message indicating the feature was deleted.
    """
    result = await DBFeature.find_one({"_id": feature_id})

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Feature id: {feature_id} not found!",
        )

    result = await result.delete()  # type: ignore  # noqa: PGH003
    if result.deleted_count != 1:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong when deleting feature id: {feature_id}!",
        )

    return {"message": f"Feature id: {feature_id} deleted!"}
