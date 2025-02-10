from typing import Dict, Optional
from .base import SQLOptimizer
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.core.config import settings

class DefaultOptimizer(SQLOptimizer):
    def __init__(self, config: Dict):
        """Initialize the default optimizer with LangChain"""
        self.llm = OpenAI(
            temperature=config.get('temperature', 0),
            model_name=config.get('model', 'gpt-4'),
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.optimization_prompt = PromptTemplate(
            input_variables=["sql", "prompt", "context"],
            template="""
            Analyze and optimize the following SQL query:
            
            SQL Query:
            {sql}
            
            Requirements:
            {prompt}
            
            Additional Context:
            {context}
            
            Please provide your response in the following JSON format:
            {{
                "issues": ["list of potential issues"],
                "optimized_sql": "optimized sql query",
                "explanation": "detailed explanation of changes"
            }}
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.optimization_prompt)
    
    async def optimize(
        self,
        sql: str,
        prompt: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Optimize SQL using LangChain"""
        try:
            result = await self.chain.arun(
                sql=sql,
                prompt=prompt,
                context=str(context or {})
            )
            
            # Parse the JSON response
            import json
            return json.loads(result)
            
        except Exception as e:
            raise Exception(f"Error optimizing SQL with default optimizer: {str(e)}")
