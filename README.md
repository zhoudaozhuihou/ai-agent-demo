# SQL Optimization AI Agent

An intelligent SQL optimization service that provides both programmatic API access and a web interface for SQL query optimization.

## Features

- Multiple SQL optimization models support (OpenAI, GitHub Copilot)
- RESTful API for programmatic access
- Web interface for interactive use
- Extensible architecture for adding new optimization models
- Project and optimization history tracking
- Comprehensive API documentation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd text-to-sql-ai-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
# API Settings
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Settings (Required for default optimizer)
OPENAI_API_KEY=your-openai-api-key

# GitHub Settings (Required for Copilot optimizer)
GITHUB_TOKEN=your-github-token

# Optimizer Settings
ACTIVE_OPTIMIZER=default  # or "copilot"

# Database
DATABASE_URL=sqlite:///./sql_app.db

# Logging
LOG_LEVEL=INFO
```

## Usage

### Starting the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### SQL Optimization

```bash
# Optimize SQL query
POST /api/v1/sql/optimize
{
    "sql": "SELECT * FROM users",
    "prompt": "Optimize query performance",
    "context": {
        "table_schema": {
            "users": {
                "columns": ["id", "name", "email"],
                "indexes": ["id", "email"]
            }
        }
    }
}
```

#### Optimizer Management

```bash
# List all available optimizers
GET /api/v1/optimizers

# Get current active optimizer
GET /api/v1/optimizers/active

# Switch to a different optimizer
POST /api/v1/optimizers/{optimizer_name}/activate
```

## Optimizer System

### Available Optimizers

1. **Default Optimizer (LangChain + OpenAI)**
   - Uses OpenAI's GPT models through LangChain
   - Requires `OPENAI_API_KEY`
   - Best for general SQL optimization tasks

2. **GitHub Copilot Optimizer**
   - Uses GitHub Copilot's API
   - Requires `GITHUB_TOKEN` with Copilot access
   - Provides code-aware SQL optimization

### Adding Custom Optimizers

1. Create a new optimizer class in `app/services/models/`:

```python
from typing import Dict, Optional
from app.services.models.base import SQLOptimizer

class CustomOptimizer(SQLOptimizer):
    def __init__(self, config: Dict):
        self.config = config
        
    async def optimize(
        self,
        sql: str,
        prompt: str,
        context: Optional[Dict] = None
    ) -> Dict:
        # Implement optimization logic
        return {
            "issues": ["list of issues"],
            "optimized_sql": "optimized query",
            "explanation": "changes made"
        }
```

2. Register the optimizer in `app/core/config.py`:

```python
# In Settings class
OPTIMIZERS: Dict[str, OptimizerConfig] = {
    # ... existing optimizers ...
    "custom": OptimizerConfig(
        name="Custom Optimizer",
        description="My custom SQL optimizer",
        config={
            "param1": "value1"
        }
    )
}
```

3. Register in the factory (`app/services/models/factory.py`):

```python
from .custom_optimizer import CustomOptimizer

class OptimizerFactory:
    _optimizers: Dict[str, Type[SQLOptimizer]] = {
        # ... existing optimizers ...
        "custom": CustomOptimizer
    }
```

### Switching Optimizers

1. **Via Environment Variable**:
```env
ACTIVE_OPTIMIZER=copilot
```

2. **Via API**:
```bash
POST /api/v1/optimizers/copilot/activate
```

3. **In Code**:
```python
from app.services.sql_optimization_service import SQLOptimizationService

# Use specific optimizer
service = SQLOptimizationService(optimizer_name="copilot")

# Use default/active optimizer
service = SQLOptimizationService()
```

## Project Structure

```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── sql_optimization.py
│       │   └── optimizers.py
│       └── api.py
├── core/
│   ├── config.py
│   └── dependencies.py
├── services/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── default_optimizer.py
│   │   └── copilot_optimizer.py
│   └── sql_optimization_service.py
└── main.py
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
