"""GUI utility functions."""

from typing import Dict, Tuple

def calculate_column_widths(
    max_lengths: Tuple[int, int],
    available_width: int,
    std_width: int,
    language: str
) -> Dict[str, int]:
    """Calculate optimal column widths for the lyrics view."""
    max_orig_length, max_trans_length = max_lengths
    
    # Calculate content-based widths (pixels per character)
    char_width = {
        "default": 10,
        "ja": 20,  # Japanese characters need more width
        "ru": 12,  # Cyrillic characters need slightly more width
        "zh": 20,  # Chinese characters need more width
    }
    pixels_per_char = char_width.get(language, char_width["default"])
    
    # Calculate minimum required widths based on content
    min_orig_width = max_orig_length * pixels_per_char
    min_trans_width = max_trans_length * pixels_per_char
    
    # Use standard width if content is smaller, otherwise use content-based width
    orig_width = max(std_width, min_orig_width)
    trans_width = max(std_width, min_trans_width)
    
    # If total width exceeds available space, scale proportionally
    total_width = orig_width + trans_width
    if total_width > available_width:
        scale_factor = available_width / total_width
        orig_width = int(orig_width * scale_factor)
        trans_width = int(trans_width * scale_factor)
    
    # Ensure minimum width
    orig_width = max(200, orig_width)
    trans_width = max(200, trans_width)
    
    return {
        "Time": 60,
        "Original Lyrics": orig_width,
        "Translated Lyrics": trans_width
    }

def center_window(window, width: int, height: int) -> None:
    """Center a window on the screen."""
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}') 