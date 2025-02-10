from typing import Dict, Any, Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class OptimizerConfig(BaseModel):
    name: str
    description: str
    config: Dict[str, Any] = {}
    enabled: bool = True

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SQL Optimization AI Agent"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = None
    
    # GitHub Settings
    GITHUB_TOKEN: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Optimizer Settings
    ACTIVE_OPTIMIZER: str = "default"  # 当前激活的优化器
    OPTIMIZERS: Dict[str, OptimizerConfig] = {
        "default": OptimizerConfig(
            name="Default LangChain",
            description="Default optimizer using LangChain and OpenAI",
            config={
                "model": "gpt-4",
                "temperature": 0
            }
        ),
        "copilot": OptimizerConfig(
            name="GitHub Copilot",
            description="SQL optimization using GitHub Copilot",
            config={
                "github_token": None
            }
        )
    }

    def get_optimizer_config(self, optimizer_name: str) -> OptimizerConfig:
        """获取指定优化器的配置"""
        return self.OPTIMIZERS.get(optimizer_name)

    def is_optimizer_enabled(self, optimizer_name: str) -> bool:
        """检查优化器是否启用"""
        config = self.get_optimizer_config(optimizer_name)
        return config is not None and config.enabled
    
    class Config:
        case_sensitive = True
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.GITHUB_TOKEN:
            self.OPTIMIZERS["copilot"].config["github_token"] = self.GITHUB_TOKEN

# Create global settings instance
settings = Settings()
