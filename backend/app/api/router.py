from fastapi import APIRouter, Depends

from app.api.routes import health_check, data_ingestion
from app.src.services.auth_service import validate_api_key


api_router = APIRouter()

api_router.include_router(
    health_check.router,
    tags=["health_check"],
    dependencies=[Depends(validate_api_key)],
)

api_router.include_router(
    data_ingestion.router,
    tags=["data_ingestion"],
    dependencies=[Depends(validate_api_key)],
)
