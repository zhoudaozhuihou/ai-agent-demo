from typing import Dict, Protocol, Optional, TypedDict, runtime_checkable

class OptimizationResult(TypedDict):
    """Type definition for optimization result"""
    issues: list[str]
    optimized_sql: str
    explanation: str

@runtime_checkable
class SQLOptimizer(Protocol):
    """Protocol for SQL optimization models"""
    
    async def optimize(
        self,
        sql: str,
        prompt: str,
        context: Optional[Dict] = None
    ) -> OptimizationResult:
        """
        Optimize SQL query using the model
        
        Args:
            sql: Original SQL query
            prompt: Natural language optimization requirements
            context: Optional context about database schema
            
        Returns:
            OptimizationResult containing:
                - issues: List of identified issues
                - optimized_sql: Optimized SQL query
                - explanation: Explanation of changes
        """
        ...
