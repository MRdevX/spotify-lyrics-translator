"""Lyrics caching functionality module."""

import os
import pickle
from typing import Dict, List, Optional

from ..config.app_config import AppConfig

class LyricsCache:
    """Manages caching of translated lyrics."""
    
    def __init__(self, cache_file: str, max_size: int):
        self.cache_file = cache_file
        self.max_size = max_size
        self.cache: Dict[str, List[Dict]] = {}
        self.load_cache()
    
    def load_cache(self) -> None:
        """Load cached lyrics from file."""
        if os.path.exists(self.cache_file) and os.path.getsize(self.cache_file) > 0:
            try:
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                os.remove(self.cache_file)
                self.cache = {}
    
    def save_cache(self) -> None:
        """Save cached lyrics to file."""
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def add_lyrics(self, song_id: str, lyrics: List[Dict]) -> None:
        """Add translated lyrics to cache."""
        self.cache[song_id] = lyrics
        if len(self.cache) > self.max_size:
            self.cache.pop(next(iter(self.cache)))
        self.save_cache()
    
    def get_lyrics(self, song_id: str) -> Optional[List[Dict]]:
        """Get cached lyrics for a song."""
        return self.cache.get(song_id) 