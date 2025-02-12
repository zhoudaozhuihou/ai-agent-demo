from typing import Optional
from tortoise import fields, models
from datetime import datetime

class QueryHistory(models.Model):
    """SQL Query History Model"""
    id = fields.IntField(pk=True)
    original_sql = fields.TextField()
    optimized_sql = fields.TextField()
    issues = fields.JSONField()
    explanation = fields.TextField()
    execution_time_ms = fields.FloatField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    database_type = fields.CharField(max_length=50)
    optimizer_used = fields.CharField(max_length=50)
    success = fields.BooleanField(default=True)
    error_message = fields.TextField(null=True)

    class Meta:
        table = "query_history"

class DatabaseConnection(models.Model):
    """Database Connection Configuration Model"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    engine = fields.CharField(max_length=50)  # postgresql, mysql, sqlite
    host = fields.CharField(max_length=255, null=True)
    port = fields.IntField(null=True)
    database = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255, null=True)
    ssl_mode = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    last_connected_at = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "database_connections"

    async def test_connection(self) -> tuple[bool, Optional[str]]:
        """Test the database connection"""
        from tortoise import Tortoise
        try:
            config = self.get_connection_config()
            await Tortoise.init(
                db_url=config["url"],
                modules={"models": ["app.models.database"]}
            )
            await Tortoise.generate_schemas()
            await Tortoise.close_connections()
            self.last_connected_at = datetime.utcnow()
            await self.save()
            return True, None
        except Exception as e:
            return False, str(e)

    def get_connection_config(self) -> dict:
        """Get database connection configuration"""
        if self.engine == "postgresql":
            url = f"postgres://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.engine == "mysql":
            url = f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        elif self.engine == "sqlite":
            url = f"sqlite://{self.database}"
        else:
            raise ValueError(f"Unsupported database engine: {self.engine}")

        return {
            "url": url,
            "engine": self.engine,
            "credentials": {
                "username": self.username,
                "password": self.password,
            } if self.username and self.password else None,
            "ssl_mode": self.ssl_mode
        }
