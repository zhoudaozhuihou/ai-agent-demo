# SQL Optimization AI Agent

An AI-powered SQL optimization service with both API and web interface.

## Features

- AI-powered SQL optimization using multiple models
- Support for multiple optimizers (OpenAI GPT, GitHub Copilot)
- Modern React-based web interface
- RESTful API
- Multi-database support
- Query history tracking
- Performance metrics

## Architecture

### Backend

- FastAPI for API development
- Tortoise ORM for database operations
- Multiple AI models for SQL optimization
- Async operations support

### Frontend

- React 17
- Material-UI v4
- Redux for state management
- Monaco Editor for SQL input
- Syntax highlighting

## Database Support

The application uses Tortoise ORM and supports multiple database engines:

### Supported Databases

- PostgreSQL (Primary support)
- MySQL (Optional)
- SQLite (Optional)

### Database Features

- Connection pooling
- Automatic schema generation
- Query history tracking
- Connection management
- SSL support
- Performance metrics collection

## Prerequisites

- Python 3.11+
- Node.js 16+
- PostgreSQL 12+ (or other supported databases)
- OpenAI API key (for GPT-based optimization)
- GitHub token (optional, for Copilot-based optimization)

## Installation

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a PostgreSQL database:
```sql
CREATE DATABASE sql_optimizer;
```

4. Configure environment variables:
```bash
cp .env.example .env
```

5. Update the .env file with your settings:
```env
DATABASE_URL=postgres://username:password@localhost:5432/sql_optimizer
OPENAI_API_KEY=your-openai-api-key
GITHUB_TOKEN=your-github-token  # Optional
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Running the Application

### Start the Backend

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Start the Frontend

```bash
cd frontend
npm start
```

The web interface will be available at http://localhost:4000

## Database Configuration

### Connection Settings

The application supports various database connection options that can be configured through environment variables or the web interface:

```env
DATABASE_URL=postgres://username:password@localhost:5432/sql_optimizer
DB_MIN_SIZE=2
DB_MAX_SIZE=10
DB_SSL=false
```

### Adding New Database Connections

You can add new database connections through the API or web interface. Required information includes:

- Database type (PostgreSQL/MySQL/SQLite)
- Host and port
- Database name
- Username and password
- SSL settings (optional)

### Query History

The application automatically tracks:

- Original SQL queries
- Optimized versions
- Performance metrics
- Optimization suggestions
- Execution times
- Error messages (if any)

## API Documentation

The API documentation is available at http://localhost:8000/docs when running the application.

Key endpoints:

- `/api/v1/sql/optimize`: Optimize SQL queries
- `/api/v1/optimizers`: Manage SQL optimizers
- `/api/v1/history`: Access query history
- `/api/v1/databases`: Manage database connections

## Security Considerations

- Database credentials are encrypted
- Support for SSL connections
- API key authentication
- Rate limiting
- Input validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
