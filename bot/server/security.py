from fastapi import Header, HTTPException
from starlette import status

from data.config import SERVER_API_KEY


def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")) -> str:
    if not x_api_key or x_api_key != SERVER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "X-API-Key"},
        )
    return x_api_key
