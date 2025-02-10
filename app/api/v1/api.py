from fastapi import APIRouter
from app.api.v1.endpoints import sql_optimization, optimizers

api_router = APIRouter()

# API Service routes (for programmatic access)
# Include SQL optimization endpoints
api_router.include_router(
    sql_optimization.router,
    prefix="/sql",
    tags=["sql-optimization"]
)

# Include optimizer management endpoints
api_router.include_router(
    optimizers.router,
    prefix="/optimizers",
    tags=["optimizers"]
)
