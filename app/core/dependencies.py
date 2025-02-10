from typing import Generator
from app.services.sql_optimization_service import SQLOptimizationService
from app.services.history_service import HistoryService

def get_sql_optimization_service() -> SQLOptimizationService:
    """Dependency for getting SQLOptimizationService instance"""
    return SQLOptimizationService()

def get_history_service() -> HistoryService:
    """Dependency for getting HistoryService instance"""
    return HistoryService()
