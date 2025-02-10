from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict
from pydantic import BaseModel
from app.services.sql_optimization_service import SQLOptimizationService
from app.core.dependencies import get_sql_optimization_service

router = APIRouter()

class SQLOptimizationRequest(BaseModel):
    sql: str
    natural_language_prompt: str
    context: Optional[Dict] = None

class SQLOptimizationResponse(BaseModel):
    original_sql: str
    issues: list[str]
    optimized_sql: str
    explanation: str

@router.post("/optimize", response_model=SQLOptimizationResponse)
async def optimize_sql(
    request: SQLOptimizationRequest,
    service: SQLOptimizationService = Depends(get_sql_optimization_service)
):
    """
    API endpoint for SQL optimization service.
    This endpoint is designed for programmatic access by other services.
    """
    try:
        result = await service.optimize_sql(
            sql=request.sql,
            prompt=request.natural_language_prompt,
            context=request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
