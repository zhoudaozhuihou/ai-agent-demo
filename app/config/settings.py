from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
import yaml
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Text-to-SQL AI Agent"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = "gpt-4"
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @classmethod
    def load_from_yaml(cls, yaml_path: str) -> "Settings":
        """Load settings from a YAML file"""
        if not os.path.exists(yaml_path):
            return cls()
            
        with open(yaml_path, 'r') as f:
            yaml_settings = yaml.safe_load(f)
            return cls(**yaml_settings)
    
    class Config:
        case_sensitive = True
        env_file = ".env"
