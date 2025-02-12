from typing import Dict, Any, Optional, TypedDict
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from functools import lru_cache

class OptimizerConfigDict(TypedDict):
    name: str
    description: str
    config: Dict[str, Any]
    enabled: bool

class OptimizerConfig(BaseModel):
    name: str
    description: str
    config: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True

    def to_dict(self) -> OptimizerConfigDict:
        return {
            "name": self.name,
            "description": self.description,
            "config": self.config,
            "enabled": self.enabled
        }

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
    
    # Database Settings
    DATABASE_URL: str = "postgres://postgres:postgres@localhost:5432/sql_optimizer"
    DB_MIN_SIZE: int = 2
    DB_MAX_SIZE: int = 10
    DB_FORCE_ROLLBACK: bool = False
    DB_SSL: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Optimizer Settings
    ACTIVE_OPTIMIZER: str = "default"
    OPTIMIZERS: Dict[str, OptimizerConfig] = Field(default_factory=lambda: {
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
    })

    def get_optimizer_config(self, optimizer_name: str) -> Optional[OptimizerConfig]:
        """Get optimizer configuration"""
        return self.OPTIMIZERS.get(optimizer_name)

    def is_optimizer_enabled(self, optimizer_name: str) -> bool:
        """Check if optimizer is enabled"""
        config = self.get_optimizer_config(optimizer_name)
        return config is not None and config.enabled
    
    class Config:
        case_sensitive = True
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.GITHUB_TOKEN:
            if "copilot" in self.OPTIMIZERS:
                self.OPTIMIZERS["copilot"].config["github_token"] = self.GITHUB_TOKEN

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Create global settings instance
settings = get_settings()
