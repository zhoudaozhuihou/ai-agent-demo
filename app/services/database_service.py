from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from app.config.settings import Settings
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, settings: Settings = Settings()):
        """Initialize database service with configuration"""
        self.settings = settings
        self.engine = create_engine(settings.DATABASE_URL)
        
    async def validate_sql(self, sql_query: str) -> bool:
        """
        Validate SQL query against database schema
        
        Args:
            sql_query: SQL query to validate
            
        Returns:
            bool: True if query is valid, False otherwise
        """
        try:
            # Create a connection
            with self.engine.connect() as connection:
                # Explain the query to check its validity
                # This will raise an exception if the query is invalid
                connection.execute(text(f"EXPLAIN {sql_query}"))
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"SQL validation error: {str(e)}")
            return False
            
    async def execute_query(self, sql_query: str) -> List[Dict]:
        """
        Execute SQL query and return results
        
        Args:
            sql_query: SQL query to execute
            
        Returns:
            List of dictionaries containing query results
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql_query))
                return [dict(row) for row in result]
                
        except SQLAlchemyError as e:
            logger.error(f"Query execution error: {str(e)}")
            raise
            
    async def get_schema_info(self) -> Dict:
        """
        Get database schema information
        
        Returns:
            Dictionary containing table and column information
        """
        # This implementation will vary based on your database type
        schema_query = """
        SELECT 
            table_name,
            column_name,
            data_type
        FROM 
            information_schema.columns
        WHERE 
            table_schema = 'public'
        """
        
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(schema_query))
                schema_info = {}
                
                for row in result:
                    table = row['table_name']
                    if table not in schema_info:
                        schema_info[table] = []
                    
                    schema_info[table].append({
                        'column': row['column_name'],
                        'type': row['data_type']
                    })
                    
                return schema_info
                
        except SQLAlchemyError as e:
            logger.error(f"Schema retrieval error: {str(e)}")
            raise
