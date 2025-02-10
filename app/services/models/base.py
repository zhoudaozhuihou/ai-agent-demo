from typing import Dict, Protocol, Optional

class SQLOptimizer(Protocol):
    """Protocol for SQL optimization models"""
    
    async def optimize(
        self,
        sql: str,
        prompt: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Optimize SQL query using the model
        
        Args:
            sql: Original SQL query
            prompt: Natural language optimization requirements
            context: Optional context about database schema
            
        Returns:
            Dict containing:
                - issues: List of identified issues
                - optimized_sql: Optimized SQL query
                - explanation: Explanation of changes
        """
        pass
