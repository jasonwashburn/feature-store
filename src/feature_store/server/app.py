"""Implements entrypoint for the Feature Store server."""
from fastapi import FastAPI

from feature_store.server.routes.features import router as features_router

app = FastAPI()
app.include_router(features_router, prefix="/features")


@app.get("/")
async def read_root() -> dict[str, str]:
    """Returns a welcome message.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to Feature Store!"}
