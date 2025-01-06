"""Spotify authentication handling module."""

import json
import os
from typing import Optional

from ..config.app_config import AppConfig

class SpotifyAuthenticator:
    """Handles Spotify authentication and cookie management."""
    
    def __init__(self, config: AppConfig):
        self.config = config
    
    def load_cookie(self) -> Optional[str]:
        """Load SP_DC cookie from config file."""
        if os.path.exists(self.config.CONFIG_FILE):
            try:
                with open(self.config.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get('sp_dc')
            except Exception:
                return None
        return None
    
    def save_cookie(self, sp_dc: str) -> None:
        """Save SP_DC cookie to config file."""
        config_dir = os.path.dirname(self.config.CONFIG_FILE)
        if config_dir:
            os.makedirs(config_dir, exist_ok=True)
        
        with open(self.config.CONFIG_FILE, 'w') as f:
            json.dump({'sp_dc': sp_dc}, f) 