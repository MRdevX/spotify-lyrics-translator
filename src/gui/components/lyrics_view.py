"""Lyrics view component for displaying and managing lyrics."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Tuple, Callable

from src.utils.time_utils import ms_to_min_sec
from src.gui.utils.gui_utils import calculate_column_widths

class LyricsView:
    """Component for displaying and managing lyrics."""

    def __init__(self, container: ttk.Frame):
        self.container = container
        self.tree: Optional[ttk.Treeview] = None
        self.tooltip: Optional[tk.Toplevel] = None
        self.language: str = ""
        self.default_widths = {
            "Time": 60,
            "Original Lyrics": 350,
            "Translated Lyrics": 350
        }
        self._init_treeview()

    def _init_treeview(self) -> None:
        """Initialize the treeview component."""
        tree_frame = ttk.Frame(self.container)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Time", "Original Lyrics", "Translated Lyrics"),
            show="headings",
            style="Treeview"
        )
        
        for col in ("Time", "Original Lyrics", "Translated Lyrics"):
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, stretch=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def bind_events(self, tooltip_callback: Callable, menu_callback: Callable) -> None:
        """Bind event handlers to the treeview."""
        self.tree.bind('<Motion>', tooltip_callback)
        self.tree.bind('<Button-3>', menu_callback)

    def clear(self) -> None:
        """Clear all items from the treeview."""
        self.tree.delete(*self.tree.get_children())

    def insert_message(self, time: str, message: str) -> None:
        """Insert a message row into the treeview."""
        self.tree.insert("", "end", values=(time, message, ""))

    def update_current_lyric(self, current_position: int) -> None:
        """Update the currently playing lyric."""
        try:
            last_index = None
            for item in self.tree.get_children():
                item_data = self.tree.item(item)
                time_parts = item_data['values'][0].split(":")
                if len(time_parts) == 2:
                    try:
                        minutes = int(time_parts[0])
                        seconds = int(time_parts[1])
                        start_time = minutes * 60000 + seconds * 1000
                        if start_time <= current_position:
                            last_index = item
                        else:
                            break
                    except (ValueError, IndexError):
                        continue
            
            if last_index:
                self.tree.selection_set(last_index)
                self.tree.see(last_index)
        except Exception as e:
            print(f"Error updating current lyric: {e}")

    def display_lyrics(self, lyrics_data: List[Dict], detected_lang: str) -> None:
        """Display lyrics in the treeview."""
        self.language = detected_lang
        self.tree.heading("Original Lyrics", text=f"Original Lyrics ({detected_lang})")

        for lyric in lyrics_data:
            if not isinstance(lyric, dict) or 'startTimeMs' not in lyric or 'words' not in lyric:
                print(f"Invalid lyric format: {lyric}")
                continue
            self.tree.insert("", "end", values=(
                ms_to_min_sec(lyric['startTimeMs']),
                lyric['words'],
                ""
            ))

    def update_translations(self, translated_lyrics: List[Dict]) -> None:
        """Update translations in the treeview."""
        for item in self.tree.get_children():
            item_data = self.tree.item(item)
            start_time = item_data['values'][0]
            original_lyrics = item_data['values'][1]
            for lyric in translated_lyrics:
                if (ms_to_min_sec(lyric['startTimeMs']) == start_time and
                    lyric['words'] == original_lyrics):
                    self.tree.set(item, column="Translated Lyrics", value=lyric['translated'])
                    break
        
        if self.tree.get_children():
            first_item = self.tree.get_children()[0]
            self.tree.set(first_item, column="Translated Lyrics",
                         value=translated_lyrics[0]['translated'])

    def adjust_column_widths(self, window_width: int) -> None:
        """Adjust column widths based on content and window size."""
        max_lengths = self._calculate_max_content_lengths()
        available_width = window_width - self.default_widths["Time"] - 50
        
        column_widths = calculate_column_widths(
            max_lengths, available_width, self.default_widths["Original Lyrics"], self.language)
        self._apply_column_widths(column_widths)

    def _calculate_max_content_lengths(self) -> Tuple[int, int]:
        """Calculate maximum content lengths for lyrics columns."""
        max_original_length = 0
        max_translated_length = 0
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            max_original_length = max(max_original_length, len(values[1]))
            max_translated_length = max(max_translated_length, len(values[2]))
        
        return max_original_length, max_translated_length

    def _apply_column_widths(self, widths: Dict[str, int]) -> None:
        """Apply calculated column widths."""
        for col, new_width in widths.items():
            old_width = self.tree.column(col)['width']
            if abs(old_width - new_width) > 5:
                self._smooth_resize(col, old_width, new_width)
            else:
                self.tree.column(col, width=new_width)

    def _smooth_resize(self, column: str, start_width: int, end_width: int, steps: int = 10) -> None:
        """Animate column resizing."""
        if steps <= 0:
            self.tree.column(column, width=end_width)
            return
        
        progress = (10 - steps) / 10
        current_width = start_width + (end_width - start_width) * progress
        self.tree.column(column, width=int(current_width))
        
        self.container.after(20, lambda: self._smooth_resize(column, start_width, end_width, steps-1))

    def reset_column_widths(self) -> None:
        """Reset columns to default widths."""
        for col, width in self.default_widths.items():
            self.tree.column(col, width=width) 