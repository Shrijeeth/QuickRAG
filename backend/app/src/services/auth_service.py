from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from app.configs.config import get_settings


api_key_header = APIKeyHeader(name="x-api-key")


def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key == get_settings().APP_API_KEY:
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key",
    )
