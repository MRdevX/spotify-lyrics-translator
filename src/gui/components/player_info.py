"""Player information component for displaying song details and progress."""

import tkinter as tk
from tkinter import ttk
from typing import Dict

from src.utils.time_utils import ms_to_min_sec
from src.gui.utils.font_manager import FontManager

class PlayerInfo:
    """Component for displaying player information and progress."""

    def __init__(self, container: ttk.Frame, font_manager: FontManager):
        self.container = container
        self.font_manager = font_manager
        self.song_label: ttk.Label
        self.album_label: ttk.Label
        self.time_label: ttk.Label
        self.progress_var: tk.DoubleVar
        self.progress_bar: ttk.Progressbar
        
        self._init_components()

    def _init_components(self) -> None:
        """Initialize all player info components."""
        # Song info frame
        song_info_frame = ttk.Frame(self.container)
        song_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left side: Song info
        song_details_frame = ttk.Frame(song_info_frame)
        song_details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Song title with Spotify green color
        self.song_label = ttk.Label(
            song_details_frame,
            text="Loading...",
            font=self.font_manager.get_font('Helvetica', 'subtitle', True),
            foreground='#1DB954'  # Spotify green
        )
        self.song_label.pack(anchor='w')
        
        self.album_label = ttk.Label(
            song_details_frame,
            text="",
            font=self.font_manager.get_font('Helvetica', 'normal')
        )
        self.album_label.pack(anchor='w')
        
        # Right side: Time info
        time_frame = ttk.Frame(song_info_frame)
        time_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.time_label = ttk.Label(
            time_frame,
            text="0:00 / 0:00",
            font=self.font_manager.get_font('Helvetica', 'normal')
        )
        self.time_label.pack(anchor='e')
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.container,
            variable=self.progress_var,
            mode='determinate',
            style="Spotify.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

    def update_song_info(self, song_data: Dict) -> None:
        """Update song information display."""
        song_name = song_data['item']['name']
        artist_name = song_data['item']['artists'][0]['name']
        album_name = song_data['item']['album']['name']
        
        song_display = f"{song_name} - {artist_name}"
        self.song_label.config(text=song_display)
        self.album_label.config(text=album_name)

    def update_progress(self, current_position: int, duration: int) -> None:
        """Update progress bar and time display."""
        current_time = ms_to_min_sec(current_position)
        total_time = ms_to_min_sec(duration)
        self.time_label.config(text=f"{current_time} / {total_time}")
        
        progress_percent = (current_position / duration) * 100 if duration > 0 else 0
        self.progress_var.set(progress_percent)

    def clear_display(self) -> None:
        """Clear the display when no song is playing."""
        self.song_label.config(text="No song playing")
        self.album_label.config(text="")
        self.time_label.config(text="0:00 / 0:00")
        self.progress_var.set(0)

    def update_fonts(self, font_manager: FontManager) -> None:
        """Update component fonts."""
        self.song_label.configure(
            font=font_manager.get_font('Helvetica', 'subtitle', True),
            foreground='#1DB954'  # Maintain Spotify green color
        )
        self.album_label.configure(font=font_manager.get_font('Helvetica', 'normal'))
        self.time_label.configure(font=font_manager.get_font('Helvetica', 'normal')) 