from fastapi import APIRouter, Depends, HTTPException
from app.services.llm_service import LLMService
from app.services.database_service import DatabaseService
from app.api.schemas import SQLQueryRequest, SQLQueryResponse
from app.monitoring.metrics import track_request_time
from typing import Optional

router = APIRouter()

@router.post("/sql", response_model=SQLQueryResponse)
@track_request_time
async def generate_sql(
    request: SQLQueryRequest,
    llm_service: LLMService = Depends(),
    db_service: DatabaseService = Depends()
):
    """
    Generate SQL from natural language query
    """
    try:
        # Generate SQL using LLM
        sql_query = await llm_service.generate_sql(request.query)
        
        # Validate SQL against database schema
        is_valid = await db_service.validate_sql(sql_query)
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Generated SQL is invalid")
            
        return SQLQueryResponse(
            natural_query=request.query,
            sql_query=sql_query,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
