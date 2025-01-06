"""Configuration settings for the Spotify Lyrics Translator application."""

import os
import sys
from dataclasses import dataclass
from typing import Optional

@dataclass
class AppConfig:
    """Configuration settings for the application."""
    APP_DATA_PATH: str
    CONFIG_FILE: str
    CACHE_FILE: str
    MAX_CACHE_SIZE: int = 1000

    @classmethod
    def create_default_config(cls) -> 'AppConfig':
        """Create default configuration based on the platform."""
        app_data_path = cls._get_app_data_path()
        return cls(
            APP_DATA_PATH=app_data_path,
            CONFIG_FILE=os.path.join(app_data_path, 'config.json'),
            CACHE_FILE=os.path.join(app_data_path, 'lyrics_cache.pkl')
        )
    
    @staticmethod
    def _get_app_data_path() -> str:
        """Get the path where app data should be stored."""
        if getattr(sys, 'frozen', False):
            if sys.platform == 'darwin':
                app_data = os.path.expanduser('~/Library/Application Support/Spotify Lyrics Translator')
            elif sys.platform == 'win32':
                app_data = os.path.join(os.environ.get('APPDATA', ''), 'Spotify Lyrics Translator')
            else:
                app_data = os.path.dirname(os.path.abspath(__file__))
        else:
            app_data = os.path.dirname(os.path.abspath(__file__))
        
        os.makedirs(app_data, exist_ok=True)
        return app_data 