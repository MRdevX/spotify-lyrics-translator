"""Main application class for Spotify Lyrics Translator."""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple

import sv_ttk
from deep_translator import GoogleTranslator
from syrics.api import Spotify

from src.config.app_config import AppConfig
from src.core.auth import SpotifyAuthenticator
from src.core.cache import LyricsCache
from src.gui.components.lyrics_view import LyricsView
from src.gui.components.player_info import PlayerInfo
from src.gui.components.dialogs import LoginDialog, AboutDialog
from src.gui.styles import configure_styles
from src.gui.utils.font_manager import FontManager

class SpotifyLyricsTranslator:
    """Main application class for Spotify Lyrics Translator."""

    def __init__(self):
        """Initialize the application."""
        try:
            self.root = tk.Tk()
            self.root.title("Spotify Lyrics Translator")
            
            # Initialize configuration
            self.config = AppConfig.create_default_config()
            
            # Initialize components
            self.authenticator = SpotifyAuthenticator(self.config)
            self.lyrics_cache = LyricsCache(self.config.CACHE_FILE, self.config.MAX_CACHE_SIZE)
            self.font_manager = FontManager()
            self.sp: Optional[Spotify] = None
            
            # GUI state variables
            self.current_song_id: Optional[str] = None
            self.translation_complete: bool = False
            self.language: str = ""
            
            self.setup_gui()
            
        except Exception as e:
            print(f"Error initializing app: {e}")
            if hasattr(self, 'root'):
                messagebox.showerror("Error", f"Failed to initialize application: {str(e)}")
            raise e

    def setup_gui(self) -> None:
        """Set up the graphical user interface."""
        # Initialize authentication
        sp_dc = self.authenticator.load_cookie()
        if sp_dc:
            try:
                self.sp = Spotify(sp_dc)
                self.sp.get_current_song()  # Test the connection
                self.initialize_main_gui()
            except Exception as e:
                messagebox.showerror("Error", f"Authentication failed: {str(e)}")
                self.show_spotify_login_dialog()
        else:
            self.show_spotify_login_dialog()

    def show_spotify_login_dialog(self) -> None:
        """Show the Spotify login dialog."""
        def on_cookie_save(cookie: str) -> None:
            try:
                print(f"\n=== Testing cookie authentication ===")
                print(f"Cookie length: {len(cookie)}")
                
                self.authenticator.save_cookie(cookie)
                print("Successfully saved cookie to config file")
                
                # Create a new instance for testing
                test_sp = Spotify(cookie)
                print("Spotify instance created successfully")
                
                # Test current song
                current_song = test_sp.get_current_song()
                if not current_song or not isinstance(current_song, dict):
                    raise Exception("Could not verify Spotify connection")
                
                print("Successfully verified connection")
                
                # Create a fresh instance for the main app
                self.sp = Spotify(cookie)
                
                # Initialize the main GUI in a separate thread to avoid EOF issues
                def delayed_init():
                    self.root.after(100, self.initialize_main_gui)
                
                threading.Thread(target=delayed_init).start()
                
            except Exception as e:
                error_message = f"""
Authentication Error

Please check:
• You're logged into Spotify in your browser
• You copied the entire cookie value
• The cookie is fresh (try logging out and back in)
• Spotify is currently playing or paused
• You have Spotify Premium (required for lyrics)

Technical details: {str(e)}
Error type: {type(e)}
"""
                print(f"Authentication error: {str(e)}")
                print(f"Error type: {type(e)}")
                messagebox.showerror("Authentication Failed", error_message)

        LoginDialog(self.root, on_cookie_save)

    def initialize_main_gui(self) -> None:
        """Initialize the main application GUI."""
        try:
            # Configure window
            self.root.geometry("900x600")
            self.root.minsize(800, 500)
            
            # Apply theme and styles
            style = ttk.Style(self.root)
            sv_ttk.set_theme("dark")
            configure_styles(style)
            
            # Create main container
            main_container = ttk.Frame(self.root, padding="10")
            main_container.pack(fill=tk.BOTH, expand=True)
            
            # Initialize components
            self.player_info = PlayerInfo(main_container, self.font_manager)
            self.lyrics_view = LyricsView(main_container, self.font_manager)
            
            # Initialize status bar
            self.status_bar = ttk.Label(
                main_container,
                text="Ready",
                font=self.font_manager.get_font('Helvetica', 'small')
            )
            self.status_bar.pack(fill=tk.X, pady=(10, 0))
            
            # Create menus
            self._init_menus()
            
            # Bind events
            self._bind_events()
            
            # Register font change callback
            self.font_manager.register_callback(self._update_fonts)
            
            # Start update loop
            self.root.after(500, self.update_display)
            
        except Exception as e:
            print(f"\n=== Error in initialize_main_gui ===")
            print(f"Error type: {type(e)}")
            print(f"Error message: {str(e)}")
            print(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No additional details'}")

    def _init_menus(self) -> None:
        """Initialize application menus."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Font size submenu
        view_menu.add_command(label="Increase Font Size", 
                            command=self._increase_font_size,
                            accelerator="Ctrl++")
        view_menu.add_command(label="Decrease Font Size", 
                            command=self._decrease_font_size,
                            accelerator="Ctrl+-")
        view_menu.add_separator()
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-plus>', lambda e: self._increase_font_size())
        self.root.bind('<Control-minus>', lambda e: self._decrease_font_size())
        self.root.bind('<Control-equal>', lambda e: self._increase_font_size())  # For keyboards without numpad

    def _increase_font_size(self) -> None:
        """Increase the font size."""
        if self.font_manager.increase_size():
            self._update_fonts()

    def _decrease_font_size(self) -> None:
        """Decrease the font size."""
        if self.font_manager.decrease_size():
            self._update_fonts()

    def _update_fonts(self) -> None:
        """Update fonts throughout the application."""
        # Update player info fonts
        self.player_info.update_fonts(self.font_manager)
        
        # Update lyrics view fonts
        self.lyrics_view.update_fonts(self.font_manager)
        
        # Adjust column widths after font change
        self.lyrics_view.adjust_column_widths(self.root.winfo_width())

    def _bind_events(self) -> None:
        """Bind event handlers."""
        self.root.bind('<Configure>', self._on_window_resize)
        self.lyrics_view.bind_events(self._show_tooltip, self._show_column_menu)

    def update_display(self) -> None:
        """Update the display with current playback information."""
        current_song, current_position = self._get_current_playback_position()
        if current_song:
            self._update_song_info(current_song, current_position)
        else:
            self._clear_display()
        
        self.root.after(500, self.update_display)

    def _get_current_playback_position(self) -> Tuple[Optional[Dict], int]:
        """Get current playback position from Spotify."""
        try:
            current_song = self.sp.get_current_song()
            position_ms = current_song['progress_ms']
            return current_song, position_ms
        except Exception as e:
            print(f"Error fetching current song playback position: {e}")
            return None, 0

    def _update_song_info(self, current_song: Dict, current_position: int) -> None:
        """Update song information and progress."""
        song_id = current_song['item']['id']
        duration = current_song['item']['duration_ms']
        
        # Update player info
        self.player_info.update_song_info(current_song)
        self.player_info.update_progress(current_position, duration)
        
        # Update lyrics if song changed
        if song_id != self.current_song_id:
            self.current_song_id = song_id
            self._update_lyrics()
        
        # Update currently playing line
        self.lyrics_view.update_current_lyric(current_position)

    def _clear_display(self) -> None:
        """Clear the display when no song is playing."""
        self.player_info.clear_display()
        self.lyrics_view.clear()
        self.lyrics_view.insert_message("0:00", "(No song playing)")

    def _update_lyrics(self) -> None:
        """Update lyrics display."""
        try:
            print("\n=== Starting lyrics update process ===")
            current_song = self.sp.get_current_song()
            print(f"Current song data retrieved: {bool(current_song)}")
            
            if not current_song or 'item' not in current_song:
                self.lyrics_view.clear()
                self.lyrics_view.insert_message("0:00", "(No song playing)")
                return
            
            song_id = current_song['item']['id']
            song_name = current_song['item']['name']
            
            lyrics = self.sp.get_lyrics(song_id)
            if not lyrics or not isinstance(lyrics, dict) or 'lyrics' not in lyrics:
                self.lyrics_view.clear()
                self.lyrics_view.insert_message("0:00", "(No lyrics available)")
                return
            
            lyrics_data = lyrics['lyrics'].get('lines', [])
            if not lyrics_data:
                self.lyrics_view.clear()
                self.lyrics_view.insert_message("0:00", "(No lyrics available)")
                return
            
            # Display lyrics
            self.lyrics_view.clear()
            self.lyrics_view.display_lyrics(lyrics_data, lyrics['lyrics'].get('language', 'unknown'))
            
            # Handle translations
            cached_lyrics = self.lyrics_cache.get_lyrics(song_id)
            if cached_lyrics:
                print("Using cached translations")
                self.lyrics_view.update_translations(cached_lyrics)
            else:
                print("Starting translation process")
                self._translate_lyrics(lyrics_data, song_name, song_id)
            
        except Exception as e:
            print(f"\n=== Error in update_lyrics ===")
            print(f"Error type: {type(e)}")
            print(f"Error message: {str(e)}")
            self.lyrics_view.clear()
            self.lyrics_view.insert_message("0:00", f"(Error: {str(e)})")

    def _translate_lyrics(self, lyrics: List[Dict], song_name: str, song_id: str) -> None:
        """Translate lyrics in a background thread."""
        def translate_line(translator: GoogleTranslator, line: Dict) -> Dict:
            original_text = line['words']
            try:
                translated_text = translator.translate(original_text)
            except Exception as e:
                print(f"Error translating '{original_text}': {e}")
                translated_text = original_text
            return {
                'startTimeMs': line['startTimeMs'],
                'words': original_text,
                'translated': translated_text
            }

        def translate():
            translator = GoogleTranslator(source='auto', target='en')
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [
                    executor.submit(translate_line, translator, line)
                    for line in lyrics
                ]
                translated_lyrics = [future.result() for future in as_completed(futures)]
            
            self.lyrics_cache.add_lyrics(song_id, translated_lyrics)
            self.root.after(0, lambda: self.lyrics_view.update_translations(translated_lyrics))

        threading.Thread(target=translate, daemon=True).start()

    def _on_window_resize(self, event: tk.Event) -> None:
        """Handle window resize event."""
        if event.widget == self.root:
            self.lyrics_view.adjust_column_widths(self.root.winfo_width())

    def _show_tooltip(self, event: tk.Event) -> None:
        """Show tooltip for truncated text."""
        # Implementation moved to LyricsView class
        pass

    def _show_column_menu(self, event: tk.Event) -> None:
        """Show column management menu."""
        # Implementation moved to LyricsView class
        pass

    def show_about_dialog(self) -> None:
        """Show the about dialog."""
        AboutDialog(self.root)

    def run(self) -> None:
        """Start the application main loop."""
        self.root.mainloop()
        # Clean up
        self.font_manager.unregister_callback(self._update_fonts) 