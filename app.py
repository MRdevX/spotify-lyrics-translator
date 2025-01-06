"""
Spotify Lyrics Translator - A desktop application that shows real-time translations of Spotify lyrics.

This module contains the main application logic for the Spotify Lyrics Translator.
It provides real-time translation of Spotify lyrics while you listen to music.

Author: Mahdi Rashidi
Email: m8rashidi@gmail.com
"""

import json
import os
import pickle
import sys
import threading
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import sv_ttk
import tkinter as tk
from deep_translator import GoogleTranslator
from syrics.api import Spotify
from tkinter import ttk, messagebox

# Type aliases
SongData = Dict[str, Any]
LyricData = Dict[str, Any]
TranslatedLyric = Dict[str, Any]

@dataclass
class AppConfig:
    """Configuration settings for the application."""
    APP_DATA_PATH: str
    CONFIG_FILE: str
    CACHE_FILE: str
    MAX_CACHE_SIZE: int = 1000

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

class LyricsCache:
    """Manages caching of translated lyrics."""
    
    def __init__(self, cache_file: str, max_size: int):
        self.cache_file = cache_file
        self.max_size = max_size
        self.cache: Dict[str, List[TranslatedLyric]] = {}
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
    
    def add_lyrics(self, song_id: str, lyrics: List[TranslatedLyric]) -> None:
        """Add translated lyrics to cache."""
        self.cache[song_id] = lyrics
        if len(self.cache) > self.max_size:
            self.cache.pop(next(iter(self.cache)))
        self.save_cache()
    
    def get_lyrics(self, song_id: str) -> Optional[List[TranslatedLyric]]:
        """Get cached lyrics for a song."""
        return self.cache.get(song_id)

class SpotifyLyricsTranslator:
    """Main application class for Spotify Lyrics Translator."""

    def __init__(self):
        """Initialize the application."""
        try:
            self.root = tk.Tk()
            self.root.title("Spotify Lyrics Translator")
            
            # Initialize configuration
            self.config = self._init_config()
            
            # Initialize components
            self.authenticator = SpotifyAuthenticator(self.config)
            self.lyrics_cache = LyricsCache(self.config.CACHE_FILE, self.config.MAX_CACHE_SIZE)
            self.sp: Optional[Spotify] = None
            
            # GUI state variables
            self.current_song_id: Optional[str] = None
            self.translation_complete: bool = False
            self.translated_lyrics_cache: Optional[List[TranslatedLyric]] = None
            self.language: str = ""
            self.tooltip: Optional[tk.Toplevel] = None
            
            self.setup_gui()
            
        except Exception as e:
            print(f"Error initializing app: {e}")
            if hasattr(self, 'root'):
                messagebox.showerror("Error", f"Failed to initialize application: {str(e)}")
            raise e

    @staticmethod
    def _init_config() -> AppConfig:
        """Initialize application configuration."""
        def get_app_data_path() -> str:
            if getattr(sys, 'frozen', False):
                if sys.platform == 'darwin':
                    app_data = os.path.expanduser('~/Library/Application Support/Spotify Lyrics Translator')
                else:
                    app_data = os.path.dirname(os.path.abspath(__file__))
            else:
                app_data = os.path.dirname(os.path.abspath(__file__))
            os.makedirs(app_data, exist_ok=True)
            return app_data
        
        app_data_path = get_app_data_path()
        return AppConfig(
            APP_DATA_PATH=app_data_path,
            CONFIG_FILE=os.path.join(app_data_path, 'config.json'),
            CACHE_FILE=os.path.join(app_data_path, 'lyrics_cache.pkl')
        )

    def setup_gui(self) -> None:
        """Set up the graphical user interface."""
        # Check Python version
        if not (sys.version_info.major == 3 and sys.version_info.minor == 11):
            self._show_python_version_error()
            sys.exit(1)
        
        # Check Tkinter
        try:
            import tkinter as tk
            from tkinter import ttk, messagebox
        except ImportError:
            self._show_tkinter_error()
            exit(1)
        
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

    @staticmethod
    def _show_python_version_error() -> None:
        """Display Python version error message."""
        print("""
Error: This application requires Python 3.11

Please install Python 3.11 and set up the environment:

macOS:
    brew install python@3.11
    brew install python-tk@3.11
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Then run the application again.
        """)

    @staticmethod
    def _show_tkinter_error() -> None:
        """Display Tkinter installation error message."""
        print("""
Error: Tkinter is not installed!

Please install Python 3.11 and Tkinter:

macOS:
    brew install python@3.11
    brew install python-tk@3.11

Ubuntu/Debian:
    sudo apt-get install python3.11-tk

Fedora:
    sudo dnf install python3.11-tkinter
        """)

    def show_spotify_login_dialog(self):
        """Show dialog with instructions to get SP_DC cookie"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Spotify Authentication")
        dialog.geometry("700x600")
        dialog.configure(bg='#282828')  # Spotify's dark theme
        dialog.transient(self.root)
        dialog.grab_set()

        # Make dialog resizable
        dialog.resizable(True, True)
        
        # Center the dialog on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

        # Main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Connect to Spotify",
            font=('Helvetica', 16, 'bold'),
            wraplength=600
        )
        title_label.pack(pady=(0, 20))

        # Step by step instructions with icons
        steps = [
            "1. Click the 'Open Spotify' button below",
            "2. Log in to Spotify if needed",
            "3. Press F12 to open Developer Tools",
            "4. Click 'Application' tab in Developer Tools",
            "5. Under 'Storage' expand 'Cookies'",
            "6. Click on 'https://spotify.com'",
            "7. Find 'sp_dc' cookie and copy its value",
            "8. Paste the value below"
        ]

        # Create frame for steps
        steps_frame = ttk.Frame(main_frame)
        steps_frame.pack(fill=tk.BOTH, padx=20, pady=10)

        for step in steps:
            step_label = ttk.Label(
                steps_frame,
                text=step,
                font=('Helvetica', 11),
                wraplength=550
            )
            step_label.pack(anchor='w', pady=5)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        def open_spotify():
            webbrowser.open('https://open.spotify.com')

        # Open Spotify button with icon
        open_button = ttk.Button(
            button_frame,
            text="Open Spotify",
            command=open_spotify,
            style='Accent.TButton'
        )
        open_button.pack(pady=10)

        # Cookie entry frame
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=10)

        # Label for cookie entry
        entry_label = ttk.Label(
            entry_frame,
            text="Paste your sp_dc cookie value here:",
            font=('Helvetica', 11)
        )
        entry_label.pack(anchor='w', pady=(0, 5))

        cookie_var = tk.StringVar()
        cookie_entry = ttk.Entry(
            entry_frame,
            textvariable=cookie_var,
            width=50,
            font=('Helvetica', 11)
        )
        cookie_entry.pack(fill=tk.X, pady=5)

        def save_cookie():
            sp_dc = cookie_var.get().strip()
            if sp_dc:
                try:
                    print(f"\n=== Testing cookie authentication ===")
                    print(f"Cookie length: {len(sp_dc)}")
                    
                    # Use the authenticator to save the cookie
                    self.authenticator.save_cookie(sp_dc)
                    print("Successfully saved cookie to config file")
                    
                    # Create a new instance for testing
                    test_sp = Spotify(sp_dc)
                    print("Spotify instance created successfully")
                    
                    # Test current song
                    current_song = test_sp.get_current_song()
                    if not current_song or not isinstance(current_song, dict):
                        raise Exception("Could not verify Spotify connection")
                    
                    print("Successfully verified connection")
                    
                    # Close the dialog first
                    dialog.destroy()
                    
                    # Create a fresh instance for the main app
                    self.sp = Spotify(sp_dc)
                    
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
            else:
                messagebox.showerror("Error", "Please enter the SP_DC cookie value.")

        # Save button with accent style
        save_button = ttk.Button(
            entry_frame,
            text="Connect",
            command=save_cookie,
            style='Accent.TButton'
        )
        save_button.pack(pady=10)

        # Help text
        help_text = ttk.Label(
            main_frame,
            text="Having trouble? Try logging out of Spotify and back in to get a fresh cookie.",
            font=('Helvetica', 10),
            wraplength=550
        )
        help_text.pack(pady=20)

    def initialize_main_gui(self) -> None:
        """Initialize the main application GUI with all components."""
        try:
            # Configure the window
            self._configure_main_window()
            
            # Initialize GUI components
            self._init_gui_components()
            
            # Start update loop
            self.root.after(500, self.update_display)
            
            # Bind events
            self._bind_events()
            
        except Exception as e:
            print(f"\n=== Error in initialize_main_gui ===")
            print(f"Error type: {type(e)}")
            print(f"Error message: {str(e)}")
            print(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No additional details'}")

    def _configure_main_window(self) -> None:
        """Configure the main window properties."""
        self.root.title("Spotify Lyrics Translator")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Apply theme and styles
        style = ttk.Style(self.root)
        sv_ttk.set_theme("dark")
        self._configure_styles(style)

    def _configure_styles(self, style: ttk.Style) -> None:
        """Configure custom styles for the application."""
        style.configure(
            "Song.TLabel",
            font=('Helvetica', 14, 'bold'),
            foreground='#1DB954'  # Spotify green
        )
        style.configure(
            "Info.TLabel",
            font=('Helvetica', 10),
            foreground='#B3B3B3'  # Spotify light gray
        )
        style.configure(
            "Treeview",
            font=('Helvetica', 11),
            rowheight=30,
            background='#282828',
            foreground='#FFFFFF',
            fieldbackground='#282828',
            borderwidth=0,
            dividerwidth=2,
            dividercolor='#404040'
        )
        style.configure(
            "Treeview.Heading",
            font=('Helvetica', 12, 'bold'),
            background='#1DB954',
            foreground='white'
        )
        style.map(
            'Treeview',
            background=[('selected', '#1DB954')],
            foreground=[('selected', 'white')]
        )

    def _init_gui_components(self) -> None:
        """Initialize all GUI components."""
        # Create main container
        self.animation_frame = ttk.Frame(self.root)
        self.animation_frame.pack(fill=tk.BOTH, expand=True)
        
        main_container = ttk.Frame(self.animation_frame, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Initialize components
        self._init_song_info(main_container)
        self._init_progress_bar(main_container)
        self._init_lyrics_view(main_container)
        self._init_status_bar(main_container)
        self._init_menus()

    def _init_song_info(self, container: ttk.Frame) -> None:
        """Initialize song information display."""
        song_info_frame = ttk.Frame(container)
        song_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left side: Song info
        song_details_frame = ttk.Frame(song_info_frame)
        song_details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.song_label = ttk.Label(
            song_details_frame,
            text="Loading...",
            style="Song.TLabel"
        )
        self.song_label.pack(anchor='w')
        
        self.album_label = ttk.Label(
            song_details_frame,
            text="",
            style="Info.TLabel"
        )
        self.album_label.pack(anchor='w')
        
        # Right side: Time info
        time_frame = ttk.Frame(song_info_frame)
        time_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.time_label = ttk.Label(
            time_frame,
            text="0:00 / 0:00",
            style="Info.TLabel"
        )
        self.time_label.pack(anchor='e')

    def _init_progress_bar(self, container: ttk.Frame) -> None:
        """Initialize progress bar."""
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            container,
            variable=self.progress_var,
            mode='determinate',
            style="Spotify.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

    def _init_lyrics_view(self, container: ttk.Frame) -> None:
        """Initialize lyrics view with treeview."""
        tree_frame = ttk.Frame(container)
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
        
        self.default_widths = {
            "Time": 60,
            "Original Lyrics": 350,
            "Translated Lyrics": 350
        }
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _init_status_bar(self, container: ttk.Frame) -> None:
        """Initialize status bar."""
        self.status_bar = ttk.Label(
            container,
            text="Ready",
            font=('Helvetica', 10),
            anchor='w'
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

    def _init_menus(self) -> None:
        """Initialize application menus."""
        self.column_menu = tk.Menu(self.root, tearoff=0)
        self.column_menu.add_command(label="Reset Column Widths", command=self.reset_column_widths)
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_dialog)

    def _bind_events(self) -> None:
        """Bind all event handlers."""
        self.tree.bind('<Motion>', self.show_tooltip)
        self.tree.bind('<Leave>', self.hide_tooltip)
        self.tree.bind('<Button-3>', self.show_column_menu)
        self.root.bind('<Configure>', self.on_window_resize)

    def update_display(self) -> None:
        """Update the display with current playback information."""
        current_song, current_position = self.get_current_playback_position()
        if current_song:
            self._update_song_info(current_song, current_position)
        else:
            self._clear_display()
        
        self.root.after(500, self.update_display)

    def _update_song_info(self, current_song: SongData, current_position: int) -> None:
        """Update song information display."""
        song_id = current_song['item']['id']
        song_name = current_song['item']['name']
        artist_name = current_song['item']['artists'][0]['name']
        album_name = current_song['item']['album']['name']
        duration = current_song['item']['duration_ms']
        
        # Update song info
        song_display = f"{song_name} - {artist_name}"
        self.song_label.config(text=song_display)
        self.album_label.config(text=album_name)
        
        # Update time and progress
        current_time = self.ms_to_min_sec(current_position)
        total_time = self.ms_to_min_sec(duration)
        self.time_label.config(text=f"{current_time} / {total_time}")
        
        # Update progress bar
        progress_percent = (current_position / duration) * 100
        self.progress_var.set(progress_percent)
        
        # Update lyrics if song changed
        if song_id != self.current_song_id:
            self.current_song_id = song_id
            self.update_lyrics()
        
        # Update currently playing line
        self.update_current_lyric(current_position)

    def _clear_display(self) -> None:
        """Clear the display when no song is playing."""
        self.song_label.config(text="No song playing")
        self.album_label.config(text="")
        self.time_label.config(text="0:00 / 0:00")
        self.progress_var.set(0)

    def save_cache(self):
        with open(self.config.CACHE_FILE, 'wb') as f:
            pickle.dump(self.lyrics_cache, f)

    def get_current_playback_position(self):
        try:
            current_song = self.sp.get_current_song()
            position_ms = current_song['progress_ms']
            return current_song, position_ms
        except Exception as e:
            print(f"Error fetching current song playback position: {e}")
            return None, 0

    def update_current_lyric(self, current_position: int) -> None:
        """Update the currently playing lyric in the tree view."""
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

    @staticmethod
    def ms_to_min_sec(ms: int) -> str:
        """Convert milliseconds to MM:SS format."""
        try:
            # Ensure ms is an integer
            ms = int(ms) if isinstance(ms, str) else ms
            minutes = ms // 60000
            seconds = (ms % 60000) // 1000
            return f"{minutes}:{seconds:02d}"
        except (ValueError, TypeError):
            return "0:00"

    def translate_line(self, translator: GoogleTranslator, line: LyricData) -> TranslatedLyric:
        """Translate a single line of lyrics."""
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

    def translate_words(self, lyrics: List[LyricData], song_name: str, song_id: str,
                       callback: callable) -> None:
        """Translate all lyrics for a song."""
        translator = GoogleTranslator(source='auto', target='en')
        translated_song_name = translator.translate(song_name)
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self.translate_line, translator, line)
                for line in lyrics
            ]
            translated_lyrics = [future.result() for future in as_completed(futures)]
        
        # Use the LyricsCache class instead of direct dictionary access
        self.lyrics_cache.add_lyrics(song_id, translated_lyrics)
        callback(translated_lyrics)
        self.translation_complete = True

    def update_lyrics(self) -> None:
        """Update lyrics display with current song lyrics."""
        try:
            print("\n=== Starting lyrics update process ===")
            current_song = self.sp.get_current_song()
            print(f"Current song data retrieved: {bool(current_song)}")
            
            if not current_song or 'item' not in current_song:
                self._handle_no_song()
                return
            
            song_id = current_song['item']['id']
            song_name = current_song['item']['name']
            artist_name = current_song['item']['artists'][0]['name']
            print(f"Song details - ID: {song_id}, Name: {song_name}, Artist: {artist_name}")
            
            lyrics = self._fetch_lyrics(song_id)
            if not lyrics:
                return
            
            self._process_lyrics(lyrics, song_id, song_name, artist_name)
            
        except Exception as e:
            self._handle_lyrics_error(e)

    def _handle_no_song(self) -> None:
        """Handle case when no song is playing."""
        print("No valid current song data")
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", "end", values=("0:00", "(No song playing)", ""))

    def _fetch_lyrics(self, song_id: str) -> Optional[Dict]:
        """Fetch lyrics from Spotify API."""
        print("Attempting to fetch lyrics...")
        try:
            lyrics = self.sp.get_lyrics(song_id)
            if not lyrics:
                print("No lyrics returned from Spotify")
                self.tree.delete(*self.tree.get_children())
                self.tree.insert("", "end", values=("0:00", "(No lyrics available)", ""))
                return None
            
            print(f"Raw lyrics response type: {type(lyrics)}")
            print(f"Raw lyrics response keys: {lyrics.keys() if isinstance(lyrics, dict) else 'Not a dictionary'}")
            return lyrics
            
        except Exception as lyrics_error:
            print(f"Error fetching lyrics: {str(lyrics_error)}")
            print(f"Error type: {type(lyrics_error)}")
            print(f"Error details: {lyrics_error.__dict__ if hasattr(lyrics_error, '__dict__') else 'No additional details'}")
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=("0:00", f"(Error: {str(lyrics_error)})", ""))
            return None

    def _process_lyrics(self, lyrics: Dict, song_id: str, song_name: str, artist_name: str) -> None:
        """Process and display lyrics data."""
        if not isinstance(lyrics, dict) or 'lyrics' not in lyrics:
            print("Invalid lyrics format - missing 'lyrics' key")
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=("0:00", "(Invalid lyrics format)", ""))
            return
            
        if not isinstance(lyrics['lyrics'], dict) or 'lines' not in lyrics['lyrics']:
            print("Invalid lyrics format - missing 'lines' key")
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=("0:00", "(Invalid lyrics format)", ""))
            return
            
        lyrics_data = lyrics['lyrics']['lines']
        print(f"Lyrics data extracted: {bool(lyrics_data)}")

        # Update song label with current song info
        song_display = f"{song_name} - {artist_name}"
        self.song_label.config(text=song_display)
        
        self.tree.delete(*self.tree.get_children())

        if lyrics_data:
            self._display_lyrics(lyrics_data, lyrics['lyrics'].get('language', 'unknown'), song_id, song_name)
        else:
            print("No lyrics data available")
            self.tree.insert("", "end", values=("0:00", "(No lyrics available)", ""))
        
        self.adjust_column_widths()

    def _display_lyrics(self, lyrics_data: List[Dict], detected_lang: str, song_id: str, song_name: str) -> None:
        """Display lyrics in the treeview."""
        print(f"Number of lyric lines: {len(lyrics_data)}")
        self.language = detected_lang
        print(f"Detected language: {detected_lang}")
        
        self.tree.heading("Original Lyrics", text=f"Original Lyrics ({detected_lang})")

        for lyric in lyrics_data:
            if not isinstance(lyric, dict) or 'startTimeMs' not in lyric or 'words' not in lyric:
                print(f"Invalid lyric format: {lyric}")
                continue
            self.tree.insert("", "end", values=(
                self.ms_to_min_sec(lyric['startTimeMs']),
                lyric['words'],
                ""
            ))
        
        self.translation_complete = False
        # Use the LyricsCache class methods
        cached_lyrics = self.lyrics_cache.get_lyrics(song_id)
        if cached_lyrics:
            print("Using cached translations")
            self.update_translations(cached_lyrics)
        else:
            print("Starting translation process")
            threading.Thread(
                target=self.translate_words,
                args=(lyrics_data, song_name, song_id, self.update_translations)
            ).start()

    def _handle_lyrics_error(self, error: Exception) -> None:
        """Handle errors in lyrics processing."""
        print(f"\n=== Error in update_lyrics ===")
        print(f"Error type: {type(error)}")
        print(f"Error message: {str(error)}")
        print(f"Error details: {error.__dict__ if hasattr(error, '__dict__') else 'No additional details'}")
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", "end", values=("0:00", f"(Error: {str(error)})", ""))

    def update_translations(self, translated_lyrics: List[TranslatedLyric]) -> None:
        """Update the translations in the treeview."""
        for item in self.tree.get_children():
            item_data = self.tree.item(item)
            start_time = item_data['values'][0]
            original_lyrics = item_data['values'][1]
            for lyric in translated_lyrics:
                if (self.ms_to_min_sec(lyric['startTimeMs']) == start_time and
                    lyric['words'] == original_lyrics):
                    self.tree.set(item, column="Translated Lyrics", value=lyric['translated'])
                    break
        
        if self.tree.get_children():
            first_item = self.tree.get_children()[0]
            self.tree.set(first_item, column="Translated Lyrics",
                         value=translated_lyrics[0]['translated'])
        
        self.adjust_column_widths()

    def adjust_column_widths(self) -> None:
        """Adjust column widths with animation."""
        # Standard fixed widths
        std_time_width = 60
        std_lyrics_width = 350  # Standard width for lyrics columns
        
        # Calculate maximum content lengths
        max_lengths = self._calculate_max_content_lengths()
        
        # Get window width and calculate available space
        window_width = self.root.winfo_width()
        available_width = window_width - std_time_width - 50  # Account for scrollbar and padding
        
        # Calculate and apply column widths
        column_widths = self._calculate_column_widths(
            max_lengths, available_width, std_lyrics_width)
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

    def _calculate_column_widths(self, max_lengths: Tuple[int, int],
                               available_width: int, std_width: int) -> Dict[str, int]:
        """Calculate optimal column widths."""
        max_orig_length, max_trans_length = max_lengths
        
        # Calculate content-based widths (pixels per character)
        char_width = {
            "default": 10,
            "ja": 20,  # Japanese characters need more width
            "ru": 12,  # Cyrillic characters need slightly more width
            "zh": 20,  # Chinese characters need more width
        }
        pixels_per_char = char_width.get(self.language, char_width["default"])
        
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

    def _apply_column_widths(self, widths: Dict[str, int]) -> None:
        """Apply calculated column widths with animation."""
        for col, new_width in widths.items():
            old_width = self.tree.column(col)['width']
            if abs(old_width - new_width) > 5:  # Only animate if change is significant
                self.smooth_resize(col, old_width, new_width)
            else:
                self.tree.column(col, width=new_width)

    def smooth_resize(self, column: str, start_width: int, end_width: int, steps: int = 10) -> None:
        """Animate column resizing."""
        if steps <= 0:
            self.tree.column(column, width=end_width)
            return
        
        # Calculate the current width using proper linear interpolation
        progress = (10 - steps) / 10  # Progress from 0 to 1
        current_width = start_width + (end_width - start_width) * progress
        self.tree.column(column, width=int(current_width))
        
        self.root.after(20, lambda: self.smooth_resize(column, start_width, end_width, steps-1))

    def show_about_dialog(self):
        """Show About dialog with application information"""
        dialog = tk.Toplevel(self.root)
        dialog.title("About Spotify Lyrics Translator")
        dialog.geometry("600x500")
        dialog.configure(bg='#282828')  # Spotify's dark theme
        dialog.transient(self.root)
        dialog.grab_set()

        # Make dialog resizable
        dialog.resizable(True, True)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

        # Main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # App title
        title_label = ttk.Label(
            main_frame,
            text="Spotify Lyrics Translator",
            font=('Helvetica', 16, 'bold'),
            wraplength=500
        )
        title_label.pack(pady=(0, 10))

        # Version
        version_label = ttk.Label(
            main_frame,
            text="Version 1.0.0",
            font=('Helvetica', 10),
        )
        version_label.pack(pady=(0, 20))

        # Description
        desc_label = ttk.Label(
            main_frame,
            text="A desktop application that shows real-time translations of Spotify lyrics while you listen to music.",
            font=('Helvetica', 11),
            wraplength=500,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 20))

        # Author info
        author_frame = ttk.Frame(main_frame)
        author_frame.pack(fill=tk.X, pady=10)

        author_label = ttk.Label(
            author_frame,
            text="Author: Mahdi Rashidi",
            font=('Helvetica', 11),
        )
        author_label.pack()

        email_label = ttk.Label(
            author_frame,
            text="Email: m8rashidi@gmail.com",
            font=('Helvetica', 11),
            cursor="hand2",
            foreground="#1DB954"  # Spotify green
        )
        email_label.pack()
        email_label.bind("<Button-1>", lambda e: webbrowser.open("mailto:m8rashidi@gmail.com"))

        # Repository link
        repo_label = ttk.Label(
            author_frame,
            text="GitHub Repository",
            font=('Helvetica', 11),
            cursor="hand2",
            foreground="#1DB954"  # Spotify green
        )
        repo_label.pack()
        repo_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/MRdevX/spotify-translator"))

        # Credits
        credits_frame = ttk.Frame(main_frame)
        credits_frame.pack(fill=tk.X, pady=20)

        credits_label = ttk.Label(
            credits_frame,
            text="Credits",
            font=('Helvetica', 12, 'bold'),
        )
        credits_label.pack()

        original_repo_label = ttk.Label(
            credits_frame,
            text="Original Project by @atahanuz",
            font=('Helvetica', 11),
            cursor="hand2",
            foreground="#1DB954"  # Spotify green
        )
        original_repo_label.pack()
        original_repo_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/atahanuz/spotify-translator"))

        # Close button
        close_button = ttk.Button(
            main_frame,
            text="Close",
            command=dialog.destroy,
            style='Accent.TButton'
        )
        close_button.pack(pady=20)

    def run(self) -> None:
        """Start the application main loop."""
        self.root.mainloop()

    def on_window_resize(self, event=None):
        """Handle window resize event"""
        if event.widget == self.root:
            self.adjust_column_widths()

    def show_tooltip(self, event):
        """Show tooltip for truncated text"""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if item and column:
            col_idx = int(column[1]) - 1
            values = self.tree.item(item)['values']
            if col_idx < len(values):
                cell_value = str(values[col_idx])
                
                # Get cell width
                col_width = self.tree.column(self.tree.heading(column)['text'])['width']
                text_width = self.tree.tk.call('font', 'measure', self.tree.cget('font'), cell_value)
                
                # Show tooltip only if text is truncated
                if text_width > col_width:
                    if self.tooltip:
                        self.tooltip.destroy()
                    
                    x, y, _, _ = self.tree.bbox(item, column)
                    x += self.tree.winfo_rootx()
                    y += self.tree.winfo_rooty()
                    
                    self.tooltip = tk.Toplevel(self.tree)
                    self.tooltip.wm_overrideredirect(True)
                    
                    label = ttk.Label(
                        self.tooltip,
                        text=cell_value,
                        background='#282828',
                        foreground='white',
                        padding=5
                    )
                    label.pack()
                    
                    self.tooltip.geometry(f"+{x}+{y+25}")

    def hide_tooltip(self, event=None):
        """Hide the tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def show_column_menu(self, event):
        """Show right-click menu for column management"""
        self.column_menu.post(event.x_root, event.y_root)

    def reset_column_widths(self):
        """Reset columns to default widths"""
        for col, width in self.default_widths.items():
            self.tree.column(col, width=width)
        self.adjust_column_widths()

if __name__ == "__main__":
    app = SpotifyLyricsTranslator()
    app.run()
