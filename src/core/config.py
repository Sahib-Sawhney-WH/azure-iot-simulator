"""
Configuration management for Azure IoT Hub Device Simulator
"""

import os
import sqlite3
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, Any

from .logging_config import get_logger

logger = get_logger('config')


@dataclass
class AppConfig:
    """Application configuration"""
    app_name: str = "Azure IoT Hub Device Simulator"
    version: str = "1.0.0"
    theme: str = "light"  # light or dark
    auto_save: bool = True
    log_level: str = "INFO"
    window_width: int = 1200
    window_height: int = 800
    data_dir: str = ""
    
    def __post_init__(self):
        if not self.data_dir:
            self.data_dir = str(Path.home() / ".azure_iot_simulator")


@dataclass
class AzureConfig:
    """Azure IoT Hub configuration"""
    connection_string: str = ""
    device_id: str = ""
    protocol: str = "MQTT"  # MQTT, AMQP, HTTPS
    auto_reconnect: bool = True
    connection_timeout: int = 30


class ConfigManager:
    """Configuration manager with SQLite persistence"""
    
    def __init__(self):
        self.app_config = AppConfig()
        self.azure_config = AzureConfig()
        
        # Ensure data directory exists
        os.makedirs(self.app_config.data_dir, exist_ok=True)
        
        # Database path
        self.db_path = os.path.join(self.app_config.data_dir, "config.db")
        
        # Initialize database and load config
        self._init_database()
        self._load_config()
    
    def _init_database(self):
        """Initialize the configuration database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create config table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS config (
                        section TEXT NOT NULL,
                        key TEXT NOT NULL,
                        value TEXT NOT NULL,
                        PRIMARY KEY (section, key)
                    )
                """)
                
                conn.commit()
                logger.info("Configuration database initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _load_config(self):
        """Load configuration from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Load app config
                cursor.execute("SELECT key, value FROM config WHERE section = 'app'")
                app_data = dict(cursor.fetchall())
                
                if app_data:
                    # Update app config with saved values
                    for key, value in app_data.items():
                        if hasattr(self.app_config, key):
                            # Convert string values to appropriate types
                            field_type = type(getattr(self.app_config, key))
                            if field_type == bool:
                                setattr(self.app_config, key, value.lower() == 'true')
                            elif field_type == int:
                                setattr(self.app_config, key, int(value))
                            else:
                                setattr(self.app_config, key, value)
                
                # Load Azure config
                cursor.execute("SELECT key, value FROM config WHERE section = 'azure'")
                azure_data = dict(cursor.fetchall())
                
                if azure_data:
                    for key, value in azure_data.items():
                        if hasattr(self.azure_config, key):
                            field_type = type(getattr(self.azure_config, key))
                            if field_type == bool:
                                setattr(self.azure_config, key, value.lower() == 'true')
                            elif field_type == int:
                                setattr(self.azure_config, key, int(value))
                            else:
                                setattr(self.azure_config, key, value)
                
                logger.info("Configuration loaded successfully")
                
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
    
    def save_config(self):
        """Save configuration to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Save app config
                app_dict = asdict(self.app_config)
                for key, value in app_dict.items():
                    cursor.execute(
                        "INSERT OR REPLACE INTO config (section, key, value) VALUES (?, ?, ?)",
                        ("app", key, str(value))
                    )
                
                # Save Azure config
                azure_dict = asdict(self.azure_config)
                for key, value in azure_dict.items():
                    cursor.execute(
                        "INSERT OR REPLACE INTO config (section, key, value) VALUES (?, ?, ?)",
                        ("azure", key, str(value))
                    )
                
                conn.commit()
                logger.info("Configuration saved successfully")
                
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def get_app_config(self) -> AppConfig:
        """Get application configuration"""
        return self.app_config
    
    def get_azure_config(self) -> AzureConfig:
        """Get Azure configuration"""
        return self.azure_config
    
    def update_app_config(self, **kwargs):
        """Update application configuration"""
        for key, value in kwargs.items():
            if hasattr(self.app_config, key):
                setattr(self.app_config, key, value)
        
        if self.app_config.auto_save:
            self.save_config()
    
    def update_azure_config(self, **kwargs):
        """Update Azure configuration"""
        for key, value in kwargs.items():
            if hasattr(self.azure_config, key):
                setattr(self.azure_config, key, value)
        
        if self.app_config.auto_save:
            self.save_config()


# Global configuration manager instance
config_manager = ConfigManager()

