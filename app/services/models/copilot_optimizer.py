import aiohttp
import json
from typing import Dict, Optional
from .base import SQLOptimizer

class CopilotOptimizer(SQLOptimizer):
    def __init__(self, config: Dict):
        """Initialize Copilot optimizer with configuration"""
        self.config = config
        self.token = None
        self.headers = {
            "Editor-Version": "vscode/1.85.1",
            "Editor-Plugin-Version": "copilot/1.138.0",
            "User-Agent": "GithubCopilot/1.138.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate,br",
            "Connection": "close",
            "Content-Type": "application/json"
        }

    async def _get_copilot_token(self, github_token: str) -> str:
        """Get Copilot access token using GitHub token"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"token {github_token}",
                **self.headers
            }
            
            async with session.get(
                "https://api.github.com/copilot_internal/v2/token",
                headers=headers
            ) as response:
                if response.status != 200:
                    raise Exception(f"Failed to get Copilot token: {await response.text()}")
                    
                data = await response.json()
                return data.get("token")

    async def _get_copilot_completion(self, prompt: str, token: str) -> str:
        """Get completion from Copilot"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {token}",
                "X-Request-Id": "0",  # You might want to generate a unique ID
                **self.headers
            }
            
            body = {
                "prompt": prompt,
                "maxTokens": 1000,
                "temperature": 0,
                "topP": 1,
                "n": 1,
                "stream": False,
                "stops": ["```"]
            }
            
            async with session.post(
                "https://api.githubcopilot.com/chat/completions",
                headers=headers,
                json=body
            ) as response:
                if response.status != 200:
                    raise Exception(f"Failed to get Copilot completion: {await response.text()}")
                    
                data = await response.json()
                return data.get("choices", [{}])[0].get("text", "")

    def _create_optimization_prompt(self, sql: str, prompt: str, context: dict) -> str:
        """Create a prompt for SQL optimization"""
        return f"""
        You are an expert SQL optimizer. Please analyze and optimize the following SQL query:
        
        SQL Query:
        ```sql
        {sql}
        ```
        
        Requirements:
        {prompt}
        
        Database Context:
        {json.dumps(context, indent=2)}
        
        Please provide your response in the following JSON format:
        {{
            "issues": ["list of issues found"],
            "optimized_sql": "the optimized SQL query",
            "explanation": "detailed explanation of changes"
        }}
        
        Response:
        ```json
        """

    async def optimize(self, sql: str, prompt: str, context: Optional[Dict] = None) -> Dict:
        """Optimize SQL using GitHub Copilot"""
        try:
            # Get fresh token if needed
            if not self.token:
                self.token = await self._get_copilot_token(self.config["github_token"])
            
            # Create optimization prompt
            optimization_prompt = self._create_optimization_prompt(
                sql=sql,
                prompt=prompt,
                context=context or {}
            )
            
            # Get completion from Copilot
            completion = await self._get_copilot_completion(
                prompt=optimization_prompt,
                token=self.token
            )
            
            # Parse response
            try:
                # Extract JSON from the completion
                json_str = completion.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            except (IndexError, json.JSONDecodeError) as e:
                raise Exception(f"Failed to parse Copilot response: {str(e)}")
            
        except Exception as e:
            # If token expired, try once more with a new token
            if "token expired" in str(e).lower() and self.token:
                self.token = None
                return await self.optimize(sql, prompt, context)
            raise
