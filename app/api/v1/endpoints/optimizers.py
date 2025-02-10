from fastapi import APIRouter, HTTPException
from typing import Dict, List
from app.services.sql_optimization_service import SQLOptimizationService
from app.core.config import settings

router = APIRouter()

@router.get("/optimizers")
async def list_optimizers() -> Dict[str, str]:
    """列出所有可用的优化器"""
    return SQLOptimizationService.list_optimizers()

@router.get("/optimizers/active")
async def get_active_optimizer() -> Dict[str, str]:
    """获取当前活动的优化器"""
    active = SQLOptimizationService.get_active_optimizer()
    return {
        "name": active,
        "description": settings.get_optimizer_config(active).description
    }

@router.post("/optimizers/{optimizer_name}/activate")
async def activate_optimizer(optimizer_name: str) -> Dict[str, str]:
    """激活指定的优化器"""
    if not settings.is_optimizer_enabled(optimizer_name):
        raise HTTPException(status_code=400, detail=f"Optimizer '{optimizer_name}' is not enabled")
    
    settings.ACTIVE_OPTIMIZER = optimizer_name
    return {"message": f"Activated optimizer: {optimizer_name}"}
