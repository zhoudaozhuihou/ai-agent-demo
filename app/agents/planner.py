from typing import Dict, List, Optional
from app.services.llm_service import LLMService
from app.services.database_service import DatabaseService
import logging

logger = logging.getLogger(__name__)

class SQLPlanner:
    def __init__(
        self,
        llm_service: LLMService,
        db_service: DatabaseService
    ):
        self.llm_service = llm_service
        self.db_service = db_service
        
    async def plan_query(
        self,
        natural_query: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Plan and generate SQL query from natural language
        
        Args:
            natural_query: Natural language query
            context: Optional context about the database
            
        Returns:
            Dictionary containing the plan and generated SQL
        """
        try:
            # Get database schema if not provided in context
            if not context or 'schema' not in context:
                schema = await self.db_service.get_schema_info()
                context = context or {}
                context['schema'] = schema
            
            # Generate SQL using LLM
            sql_query = await self.llm_service.generate_sql(
                natural_query,
                context
            )
            
            # Validate the generated SQL
            is_valid = await self.db_service.validate_sql(sql_query)
            
            if not is_valid:
                raise ValueError("Generated SQL is invalid")
                
            return {
                "natural_query": natural_query,
                "sql_query": sql_query,
                "context_used": context,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error in query planning: {str(e)}")
            raise
