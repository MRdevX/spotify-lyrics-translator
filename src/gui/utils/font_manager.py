"""Font size management utilities."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable

class FontManager:
    """Manages font sizes for the application."""
    
    def __init__(self):
        # Base font sizes for different categories
        self.size_ratios = {
            'title': 1.8,      # Largest text
            'subtitle': 1.3,   # Song titles
            'normal': 1.0,     # Regular text
            'small': 0.9       # Status text
        }
        
        # Base size (normal text size)
        self.base_size = 11
        
        # Size limits
        self.min_base_size = 8
        self.max_base_size = 24
        
        self.callbacks: List[Callable] = []
    
    def get_font_size(self, category: str) -> int:
        """Get the current font size for a category."""
        ratio = self.size_ratios.get(category, 1.0)
        return int(self.base_size * ratio)
    
    def increase_size(self) -> bool:
        """Increase the font size."""
        if self.base_size < self.max_base_size:
            self.base_size += 1
            self._notify_change()
            return True
        return False
    
    def decrease_size(self) -> bool:
        """Decrease the font size."""
        if self.base_size > self.min_base_size:
            self.base_size -= 1
            self._notify_change()
            return True
        return False
    
    def register_callback(self, callback: Callable) -> None:
        """Register a callback for font size changes."""
        if callback not in self.callbacks:
            self.callbacks.append(callback)
    
    def unregister_callback(self, callback: Callable) -> None:
        """Unregister a callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _notify_change(self) -> None:
        """Notify all registered callbacks of font size change."""
        for callback in self.callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in font size change callback: {e}")
    
    def get_font(self, family: str, category: str, bold: bool = False) -> tuple:
        """Get a font tuple for the specified category."""
        size = self.get_font_size(category)
        weight = 'bold' if bold else 'normal'
        return (family, size, weight) 