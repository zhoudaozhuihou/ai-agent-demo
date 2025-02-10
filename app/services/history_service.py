from typing import Optional, List, Dict
from datetime import datetime
import uuid

class HistoryService:
    def __init__(self):
        """Initialize the history service"""
        # TODO: Replace with proper database storage
        self._history = []
        self._projects = {}
    
    async def save_optimization(
        self,
        project_id: Optional[str],
        original_sql: str,
        optimized_sql: str,
        tags: Optional[List[str]] = None
    ) -> str:
        """Save an optimization result to history"""
        request_id = str(uuid.uuid4())
        
        record = {
            "id": request_id,
            "project_id": project_id,
            "original_sql": original_sql,
            "optimized_sql": optimized_sql,
            "tags": tags or [],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self._history.append(record)
        
        if project_id:
            if project_id not in self._projects:
                self._projects[project_id] = {
                    "id": project_id,
                    "name": f"Project {project_id}",
                    "created_at": datetime.utcnow().isoformat()
                }
        
        return request_id
    
    async def get_history(
        self,
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict]:
        """Get optimization history with optional filters"""
        filtered = self._history
        
        if project_id:
            filtered = [h for h in filtered if h["project_id"] == project_id]
            
        if tags:
            filtered = [
                h for h in filtered 
                if any(tag in h["tags"] for tag in tags)
            ]
            
        return sorted(
            filtered,
            key=lambda x: x["timestamp"],
            reverse=True
        )
    
    async def get_projects(self) -> List[Dict]:
        """Get list of all projects"""
        return list(self._projects.values())
