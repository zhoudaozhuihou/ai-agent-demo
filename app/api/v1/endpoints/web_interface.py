from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional, Dict, List
from pydantic import BaseModel
from app.services.sql_optimization_service import SQLOptimizationService
from app.services.history_service import HistoryService
from app.core.dependencies import get_sql_optimization_service, get_history_service

router = APIRouter()

class WebOptimizationRequest(BaseModel):
    sql: str
    natural_language_prompt: str
    project_id: Optional[str] = None
    tags: Optional[List[str]] = None

class WebOptimizationResponse(BaseModel):
    request_id: str
    original_sql: str
    issues: list[str]
    optimized_sql: str
    explanation: str
    visualization: Optional[Dict] = None  # For future visualization features
    execution_plan: Optional[Dict] = None  # For future execution plan features

@router.post("/web/optimize", response_model=WebOptimizationResponse)
async def web_optimize_sql(
    request: WebOptimizationRequest,
    sql_service: SQLOptimizationService = Depends(get_sql_optimization_service),
    history_service: HistoryService = Depends(get_history_service)
):
    """
    Web interface endpoint for SQL optimization.
    This endpoint includes additional features like history tracking and visualization
    specifically designed for web UI consumption.
    """
    try:
        # Optimize SQL
        optimization_result = await sql_service.optimize_sql(
            sql=request.sql,
            prompt=request.natural_language_prompt
        )
        
        # Save to history
        request_id = await history_service.save_optimization(
            project_id=request.project_id,
            original_sql=request.sql,
            optimized_sql=optimization_result.optimized_sql,
            tags=request.tags
        )
        
        # Prepare web-specific response
        return WebOptimizationResponse(
            request_id=request_id,
            **optimization_result.dict(),
            visualization=await sql_service.generate_visualization(optimization_result.optimized_sql),
            execution_plan=await sql_service.get_execution_plan(optimization_result.optimized_sql)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/web/history")
async def get_optimization_history(
    project_id: Optional[str] = None,
    tags: Optional[List[str]] = None,
    history_service: HistoryService = Depends(get_history_service)
):
    """Get optimization history for web interface"""
    return await history_service.get_history(project_id=project_id, tags=tags)

@router.get("/web/projects")
async def get_projects(
    history_service: HistoryService = Depends(get_history_service)
):
    """Get list of projects for web interface"""
    return await history_service.get_projects()
