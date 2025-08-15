"""Template manager for message templates"""
import json
import sqlite3
from typing import Dict, List, Optional
from core.logging_config import get_logger

logger = get_logger('template_manager')

class TemplateManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize templates database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS templates (
                    name TEXT PRIMARY KEY,
                    description TEXT,
                    template_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def save_template(self, name: str, description: str, template_data: dict) -> bool:
        """Save a message template"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO templates (name, description, template_data, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (name, description, json.dumps(template_data)))
            logger.info(f"Saved template: {name}")
            return True
        except Exception as e:
            logger.error(f"Error saving template {name}: {e}")
            return False
    
    def load_template(self, name: str) -> Optional[dict]:
        """Load a message template"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT template_data FROM templates WHERE name = ?', (name,))
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
            return None
        except Exception as e:
            logger.error(f"Error loading template {name}: {e}")
            return None
    
    def list_templates(self) -> List[dict]:
        """List all templates"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT name, description, created_at FROM templates ORDER BY name')
                return [{"name": row[0], "description": row[1], "created_at": row[2]} for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error listing templates: {e}")
            return []
    
    def delete_template(self, name: str) -> bool:
        """Delete a template"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM templates WHERE name = ?', (name,))
            logger.info(f"Deleted template: {name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting template {name}: {e}")
            return False
