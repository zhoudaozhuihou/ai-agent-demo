from typing import Optional
from tortoise import Tortoise
from app.core.config import settings

async def init_db() -> None:
    """Initialize database connection"""
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["app.models.database"]}
    )
    # Generate schemas
    await Tortoise.generate_schemas()

async def close_db() -> None:
    """Close database connection"""
    await Tortoise.close_connections()

async def get_connection_by_id(connection_id: int) -> Optional[dict]:
    """Get database connection configuration by ID"""
    from app.models.database import DatabaseConnection
    connection = await DatabaseConnection.get_or_none(id=connection_id)
    if connection:
        return connection.get_connection_config()
    return None

async def test_connection(config: dict) -> tuple[bool, Optional[str]]:
    """Test database connection with given configuration"""
    try:
        await Tortoise.init(
            db_url=config["url"],
            modules={"models": ["app.models.database"]}
        )
        await Tortoise.generate_schemas()
        await Tortoise.close_connections()
        return True, None
    except Exception as e:
        return False, str(e)

class DatabaseManager:
    """Database connection manager"""
    def __init__(self):
        self._connections = {}

    async def get_connection(self, connection_id: int) -> Optional[dict]:
        """Get or create database connection"""
        if connection_id not in self._connections:
            config = await get_connection_by_id(connection_id)
            if config:
                self._connections[connection_id] = config
        return self._connections.get(connection_id)

    async def close_connection(self, connection_id: int) -> None:
        """Close database connection"""
        if connection_id in self._connections:
            del self._connections[connection_id]

    async def close_all(self) -> None:
        """Close all database connections"""
        self._connections.clear()
        await close_db()

# Create global database manager instance
db_manager = DatabaseManager()
