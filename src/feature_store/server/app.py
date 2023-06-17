"""Implements entrypoint for the Feature Store server."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    """Returns a welcome message.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to Feature Store!"}
