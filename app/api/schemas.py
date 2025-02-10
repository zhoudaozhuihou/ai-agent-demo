from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class SQLQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query to convert to SQL")
    context: Optional[Dict] = Field(default=None, description="Additional context for SQL generation")
    
    class Config:
        schema_extra = {
            "example": {
                "query": "Show me all users who signed up last month",
                "context": {
                    "table": "users",
                    "relevant_columns": ["id", "signup_date", "email"]
                }
            }
        }

class SQLQueryResponse(BaseModel):
    natural_query: str = Field(..., description="Original natural language query")
    sql_query: str = Field(..., description="Generated SQL query")
    status: str = Field(..., description="Status of the query generation")
    explanation: Optional[str] = Field(None, description="Explanation of the generated SQL")
    
    class Config:
        schema_extra = {
            "example": {
                "natural_query": "Show me all users who signed up last month",
                "sql_query": "SELECT * FROM users WHERE signup_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)",
                "status": "success",
                "explanation": "This query selects all columns from the users table where the signup date is within the last month"
            }
        }
