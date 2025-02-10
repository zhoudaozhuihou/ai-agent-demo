from typing import Optional, Dict
from app.config.settings import Settings
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, settings: Settings = Settings()):
        """Initialize LLM service with configuration"""
        self.settings = settings
        self.llm = OpenAI(
            temperature=0,
            model_name=settings.DEFAULT_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Define prompt template for SQL generation
        self.sql_prompt = PromptTemplate(
            input_variables=["query", "context"],
            template="""
            Generate a SQL query for the following natural language request:
            {query}
            
            Additional context:
            {context}
            
            Return only the SQL query without any explanation.
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.sql_prompt)
        
    async def generate_sql(self, query: str, context: Optional[Dict] = None) -> str:
        """
        Generate SQL query from natural language input
        
        Args:
            query: Natural language query
            context: Optional context about the database schema
            
        Returns:
            Generated SQL query
        """
        try:
            context = context or {}
            result = await self.chain.arun(query=query, context=str(context))
            
            # Clean and validate the generated SQL
            sql_query = self._clean_sql(result)
            return sql_query
            
        except Exception as e:
            logger.error(f"Error generating SQL: {str(e)}")
            raise
            
    def _clean_sql(self, sql: str) -> str:
        """Clean and format the generated SQL query"""
        # Remove any markdown formatting if present
        sql = sql.replace("```sql", "").replace("```", "")
        
        # Remove leading/trailing whitespace
        sql = sql.strip()
        
        return sql
