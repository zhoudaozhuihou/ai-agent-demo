from typing import Dict, List, Optional, Any
from app.services.database_service import DatabaseService
import sqlparse
import logging

logger = logging.getLogger(__name__)

class SQLTools:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        
    async def analyze_query(self, sql_query: str) -> Dict[str, Any]:
        """
        Analyze SQL query for potential issues and optimization
        
        Args:
            sql_query: SQL query to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            analysis = {
                "complexity": self._assess_complexity(sql_query),
                "tables": self._extract_tables(sql_query),
                "operations": self._identify_operations(sql_query),
                "suggestions": []
            }
            
            # Add optimization suggestions
            analysis["suggestions"] = self._generate_suggestions(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing query: {str(e)}")
            raise
            
    def _assess_complexity(self, sql_query: str) -> str:
        """Assess query complexity"""
        parsed = sqlparse.parse(sql_query)[0]
        
        # Count joins
        join_count = sql_query.lower().count("join")
        
        # Count conditions
        where_count = len([
            token for token in parsed.tokens
            if isinstance(token, sqlparse.sql.Where)
        ])
        
        # Determine complexity
        if join_count > 3 or where_count > 3:
            return "high"
        elif join_count > 1 or where_count > 1:
            return "medium"
        else:
            return "low"
            
    def _extract_tables(self, sql_query: str) -> List[str]:
        """Extract table names from query"""
        parsed = sqlparse.parse(sql_query)[0]
        tables = []
        
        # Extract table names from FROM and JOIN clauses
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.Token):
                if token.value.lower() == "from":
                    # Get next token containing table name
                    next_token = parsed.token_next(
                        parsed.token_index(token)
                    )[1]
                    if next_token:
                        tables.append(str(next_token))
                        
        return tables
        
    def _identify_operations(self, sql_query: str) -> List[str]:
        """Identify SQL operations in query"""
        operations = []
        query_lower = sql_query.lower()
        
        # Check for common operations
        if "select" in query_lower:
            operations.append("select")
        if "join" in query_lower:
            operations.append("join")
        if "where" in query_lower:
            operations.append("filter")
        if "group by" in query_lower:
            operations.append("aggregate")
        if "order by" in query_lower:
            operations.append("sort")
            
        return operations
        
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """Generate optimization suggestions based on analysis"""
        suggestions = []
        
        # Complexity-based suggestions
        if analysis["complexity"] == "high":
            suggestions.append(
                "Consider breaking down complex joins into smaller queries"
            )
            
        # Operation-based suggestions
        if "join" in analysis["operations"]:
            suggestions.append(
                "Ensure proper indexing on join columns"
            )
        if "aggregate" in analysis["operations"]:
            suggestions.append(
                "Consider materialized views for frequent aggregations"
            )
            
        return suggestions
        
    async def validate_schema_compatibility(
        self,
        sql_query: str,
        schema_info: Dict
    ) -> bool:
        """
        Validate query compatibility with schema
        
        Args:
            sql_query: SQL query to validate
            schema_info: Database schema information
            
        Returns:
            bool: True if query is compatible with schema
        """
        try:
            # Extract tables and columns from query
            tables = self._extract_tables(sql_query)
            
            # Check if all tables exist in schema
            for table in tables:
                if table not in schema_info:
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(
                f"Error validating schema compatibility: {str(e)}"
            )
            return False
