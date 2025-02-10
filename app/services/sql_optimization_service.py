from typing import Dict, Optional, List
from app.services.models.factory import OptimizerFactory
from app.core.config import settings
from pydantic import BaseModel

class OptimizationResult(BaseModel):
    original_sql: str
    issues: List[str]
    optimized_sql: str
    explanation: str

class SQLOptimizationService:
    def __init__(self, optimizer_name: Optional[str] = None):
        """
        Initialize the SQL optimization service
        
        Args:
            optimizer_name: Optional, specify the name of the optimizer to use
        """
        self.optimizer = OptimizerFactory.create(optimizer_name)
        
    @classmethod
    def list_optimizers(cls) -> Dict[str, str]:
        """List all available optimizers"""
        return OptimizerFactory.list_available()
    
    @classmethod
    def get_active_optimizer(cls) -> str:
        """Get the name of the current active optimizer"""
        return settings.ACTIVE_OPTIMIZER
    
    async def optimize_sql(
        self,
        sql: str,
        prompt: str,
        context: Optional[Dict] = None
    ) -> OptimizationResult:
        """Optimize the SQL query using the current optimizer"""
        result = await self.optimizer.optimize(sql, prompt, context)
        
        return OptimizationResult(
            original_sql=sql,
            issues=result["issues"],
            optimized_sql=result["optimized_sql"],
            explanation=result["explanation"]
        )
    
    async def generate_visualization(self, sql: str) -> Optional[Dict]:
        """Generate visualization data for the SQL query (placeholder)"""
        # TODO: Implement visualization logic
        return None
    
    async def get_execution_plan(self, sql: str) -> Optional[Dict]:
        """Get the execution plan for the SQL query (placeholder)"""
        # TODO: Implement execution plan retrieval
        return None
