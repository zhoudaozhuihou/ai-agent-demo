from typing import Dict, List, Optional
import json
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class QueryMemory:
    def __init__(self, memory_file: str = "query_memory.json"):
        """Initialize query memory"""
        self.memory_file = memory_file
        self.memory = self._load_memory()
        
    def _load_memory(self) -> Dict:
        """Load memory from file"""
        try:
            memory_path = Path(self.memory_file)
            if memory_path.exists():
                with open(memory_path, 'r') as f:
                    return json.load(f)
            return {
                "queries": [],
                "patterns": {},
                "metadata": {
                    "last_updated": datetime.utcnow().isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Error loading memory: {str(e)}")
            return {
                "queries": [],
                "patterns": {},
                "metadata": {
                    "last_updated": datetime.utcnow().isoformat()
                }
            }
            
    def _save_memory(self) -> None:
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving memory: {str(e)}")
            
    def add_query(
        self,
        natural_query: str,
        sql_query: str,
        success: bool = True,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Add a query to memory
        
        Args:
            natural_query: Natural language query
            sql_query: Generated SQL query
            success: Whether the query was successful
            metadata: Additional metadata about the query
        """
        try:
            query_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "natural_query": natural_query,
                "sql_query": sql_query,
                "success": success,
                "metadata": metadata or {}
            }
            
            self.memory["queries"].append(query_entry)
            self._update_patterns(query_entry)
            self._save_memory()
            
        except Exception as e:
            logger.error(f"Error adding query to memory: {str(e)}")
            
    def _update_patterns(self, query_entry: Dict) -> None:
        """Update pattern recognition based on new query"""
        if not query_entry["success"]:
            return
            
        # Simple pattern recognition based on query structure
        natural_query = query_entry["natural_query"].lower()
        sql_query = query_entry["sql_query"]
        
        # Update pattern frequencies
        for pattern in self._extract_patterns(natural_query):
            if pattern not in self.memory["patterns"]:
                self.memory["patterns"][pattern] = {
                    "count": 0,
                    "examples": []
                }
            
            self.memory["patterns"][pattern]["count"] += 1
            self.memory["patterns"][pattern]["examples"].append({
                "natural_query": natural_query,
                "sql_query": sql_query
            })
            
    def _extract_patterns(self, query: str) -> List[str]:
        """Extract patterns from query for recognition"""
        # This is a simple implementation
        # Could be enhanced with more sophisticated pattern recognition
        patterns = []
        
        # Common SQL operation patterns
        if "show" in query or "list" in query:
            patterns.append("select_pattern")
        if "count" in query:
            patterns.append("aggregate_pattern")
        if "greater than" in query or "less than" in query:
            patterns.append("comparison_pattern")
            
        return patterns
        
    def get_similar_queries(
        self,
        natural_query: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Get similar queries from memory
        
        Args:
            natural_query: Natural language query to find similar ones
            limit: Maximum number of similar queries to return
            
        Returns:
            List of similar queries with their SQL
        """
        try:
            # Simple similarity based on common words
            query_words = set(natural_query.lower().split())
            
            similar_queries = []
            for query in self.memory["queries"]:
                stored_words = set(
                    query["natural_query"].lower().split()
                )
                similarity = len(
                    query_words.intersection(stored_words)
                ) / len(query_words.union(stored_words))
                
                if similarity > 0.3:  # Arbitrary threshold
                    similar_queries.append({
                        "natural_query": query["natural_query"],
                        "sql_query": query["sql_query"],
                        "similarity": similarity
                    })
                    
            # Sort by similarity and return top matches
            similar_queries.sort(
                key=lambda x: x["similarity"],
                reverse=True
            )
            return similar_queries[:limit]
            
        except Exception as e:
            logger.error(f"Error finding similar queries: {str(e)}")
            return []
