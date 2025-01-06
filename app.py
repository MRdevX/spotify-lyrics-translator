import sys

# Check Python version before anything else
if not (sys.version_info.major == 3 and sys.version_info.minor == 11):
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
    sys.exit(1)

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    
    # Check Tk version
    root = tk.Tk()
    tk_version = root.tk.call('info', 'patchlevel')
    root.destroy()
    
    if tk_version.startswith('9'):
        print("""
Warning: Incompatible Tk version detected (9.x)
Please install Tk 8.6 with Python 3.11:

macOS:
    brew install python@3.11
    brew install python-tk@3.11
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Ubuntu/Debian:
    sudo apt-get install python3.11-tk
        """)
        exit(1)
        
except ImportError:
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
    exit(1)

from deep_translator import GoogleTranslator
from syrics.api import Spotify
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import pickle
import os
import sv_ttk
import webbrowser
import json

# Constants
CONFIG_FILE = 'config.json'
CACHE_FILE = 'lyrics_cache.pkl'
MAX_CACHE_SIZE = 1000

class SpotifyLyricsTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spotify Lyrics Translator")
        self.sp = None
        self.setup_gui()
        
    def setup_gui(self):
        # Initialize the authentication first
        sp_dc = self.load_or_get_spotify_cookie()
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

    def load_or_get_spotify_cookie(self):
        """Load SP_DC cookie from config file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get('sp_dc')
            except Exception:
                return None
        return None

    def show_spotify_login_dialog(self):
        """Show dialog with instructions to get SP_DC cookie"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Spotify Authentication")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        instructions = """
        To use this app, you need to get your Spotify SP_DC cookie:
        
        1. Click the 'Open Spotify' button below
        2. Log in to Spotify if needed
        3. Press F12 to open Developer Tools
        4. Go to Application > Cookies > https://spotify.com
        5. Find 'sp_dc' cookie and copy its value
        6. Paste the value in the field below

        Note: Make sure to:
        - Copy the entire cookie value
        - Be logged into Spotify in your browser
        - Use a fresh cookie value (try logging out and back in to Spotify)
        """
        
        label = ttk.Label(dialog, text=instructions, wraplength=550)
        label.pack(pady=20)
        
        def open_spotify():
            webbrowser.open('https://open.spotify.com')
        
        open_button = ttk.Button(dialog, text="Open Spotify", command=open_spotify)
        open_button.pack(pady=10)
        
        cookie_var = tk.StringVar()
        cookie_entry = ttk.Entry(dialog, textvariable=cookie_var, width=50)
        cookie_entry.pack(pady=10)
        
        def save_cookie():
            sp_dc = cookie_var.get().strip()
            if sp_dc:
                try:
                    print(f"Attempting to initialize Spotify with cookie length: {len(sp_dc)}")
                    # Test the cookie
                    self.sp = Spotify(sp_dc)
                    
                    # Try to get current song to verify authentication
                    try:
                        current_song = self.sp.get_current_song()
                        if current_song:
                            print("Successfully retrieved current song")
                        else:
                            raise Exception("Could not retrieve current song")
                    except Exception as song_error:
                        print(f"Error getting current song: {str(song_error)}")
                        raise Exception(f"Could not verify Spotify connection: {str(song_error)}")
                    
                    # Save to config if valid
                    config_dir = os.path.dirname(CONFIG_FILE)
                    if config_dir:  # Only create directory if CONFIG_FILE has a directory part
                        os.makedirs(config_dir, exist_ok=True)
                    
                    with open(CONFIG_FILE, 'w') as f:
                        json.dump({'sp_dc': sp_dc}, f)
                    
                    print("Successfully saved cookie to config file")
                    dialog.destroy()
                    self.initialize_main_gui()
                except Exception as e:
                    error_message = f"""
Authentication Error: {str(e)}

Please try:
1. Logging out of Spotify in your browser
2. Logging back in
3. Getting a fresh sp_dc cookie value
4. Make sure you're copying the entire cookie value

If the problem persists, try using a private/incognito window to log in to Spotify.
"""
                    print(f"Authentication error: {str(e)}")
                    messagebox.showerror("Error", error_message)
            else:
                messagebox.showerror("Error", "Please enter the SP_DC cookie value.")
        
        save_button = ttk.Button(dialog, text="Save", command=save_cookie)
        save_button.pack(pady=10)

    def initialize_main_gui(self):
        """Initialize the main application GUI"""
        # Apply theme
        style = ttk.Style(self.root)
        style.theme_use("default")
        style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), background='#4CAF50', foreground='white')
        style.configure("Treeview", font=('Arial', 14), rowheight=40, background='#E8F5E9', foreground='black', fieldbackground='#E8F5E9')
        sv_ttk.set_theme("dark")
        style.configure("Treeview", rowheight=25)
        style.map('Treeview', background=[('selected', '#81C784')], foreground=[('selected', 'white')])
        
        # Force update of the Treeview style
        self.root.update_idletasks()
        
        # Current time label
        self.current_time_label = tk.Label(self.root, text="Current Time: 00:00", font=('Helvetica', 12, 'bold'), 
                                         bg='#388E3C', fg='#fff', padx=10, pady=5)
        self.current_time_label.pack(side=tk.TOP, fill=tk.X)
        
        # Create a frame to hold the Treeview and Scrollbar
        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and pack the treeview widget
        style.configure("Treeview.Heading", foreground="lightgreen", font=('Helvetica', 14, 'bold'))
        
        self.tree = ttk.Treeview(frame, columns=("Time", "Original Lyrics", "Translated Lyrics"), 
                                show="headings", style="Treeview")
        self.tree.heading("Time", text="  Time", anchor='w')
        self.tree.heading("Original Lyrics", text="  Original Lyrics", anchor='w')
        self.tree.heading("Translated Lyrics", text="  Translated Lyrics", anchor='w')
        self.tree.column("Time", width=200, minwidth=200, anchor='w')
        self.tree.column("Original Lyrics", width=250, anchor='w')
        self.tree.column("Translated Lyrics", width=250, anchor='w')
        
        # Create the Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill=tk.BOTH, expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initialize variables
        self.current_song_id = None
        self.translation_complete = False
        self.translated_lyrics_cache = None
        self.language = ""
        
        # Load cache
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as f:
                self.lyrics_cache = pickle.load(f)
        else:
            self.lyrics_cache = {}
        
        # Start the update loop
        self.root.after(500, self.update_display)

    def save_cache(self):
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(self.lyrics_cache, f)

    def get_current_playback_position(self):
        try:
            current_song = self.sp.get_current_song()
            position_ms = current_song['progress_ms']
            return current_song, position_ms
        except Exception as e:
            print(f"Error fetching current song playback position: {e}")
            return None, 0

    def update_display(self):
        current_song, current_position = self.get_current_playback_position()
        if current_song:
            song_id = current_song['item']['id']
            if song_id != self.current_song_id:
                self.current_song_id = song_id
                self.update_lyrics()

            self.current_time_label.config(text=f"Current Time: {self.ms_to_min_sec(current_position)}")
            last_index = None
            for item in self.tree.get_children():
                item_data = self.tree.item(item)
                start_time = int(item_data['values'][0].split(":")[0]) * 60000 + int(item_data['values'][0].split(":")[1]) * 1000
                if start_time <= current_position:
                    last_index = item
                else:
                    break
            if last_index:
                self.tree.selection_set(last_index)
                self.tree.see(last_index)

        self.root.after(500, self.update_display)

    def ms_to_min_sec(self, ms):
        ms = int(ms)
        minutes = ms // 60000
        seconds = (ms % 60000) // 1000
        return f"{minutes}:{seconds:02}"

    def translate_line(self, translator, line):
        original_text = line['words']
        try:
            translated_text = translator.translate(original_text)
        except Exception as e:
            print(f"Error translating '{original_text}': {e}")
            translated_text = original_text
        return {'startTimeMs': line['startTimeMs'], 'words': original_text, 'translated': translated_text}

    def translate_words(self, lyrics, song_name, song_id, callback):
        translator = GoogleTranslator(source='auto', target='en')
        translated_song_name = translator.translate(song_name)
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(self.translate_line, translator, line) for line in lyrics]
            translated_lyrics = [future.result() for future in as_completed(futures)]
        self.lyrics_cache[song_id] = translated_lyrics

        if len(self.lyrics_cache) > MAX_CACHE_SIZE:
            self.lyrics_cache.pop(next(iter(self.lyrics_cache)))

        self.save_cache()
        callback(translated_lyrics)
        self.translation_complete = True

    def update_lyrics(self):
        current_song = self.sp.get_current_song()
        song_id = current_song['item']['id']
        song_name = current_song['item']['name']
        lyrics = self.sp.get_lyrics(song_id)
        lyrics_data = lyrics['lyrics']['lines'] if lyrics and 'lyrics' in lyrics and 'lines' in lyrics['lyrics'] else None

        self.root.title(f"{song_name}")
        self.tree.delete(*self.tree.get_children())

        if lyrics_data:
            detected_lang = lyrics['lyrics']['language']
            self.language = detected_lang
            self.tree.heading("Original Lyrics", text=f"Original Lyrics ({detected_lang})")

            for lyric in lyrics_data:
                self.tree.insert("", "end", values=(self.ms_to_min_sec(lyric['startTimeMs']), lyric['words'], ""))
            self.translation_complete = False
            if song_id in self.lyrics_cache:
                self.update_translations(self.lyrics_cache[song_id])
            else:
                threading.Thread(target=self.translate_words, 
                              args=(lyrics_data, song_name, song_id, self.update_translations)).start()
        else:
            self.tree.insert("", "end", values=("0:00", "(No lyrics)", ""))
        self.adjust_column_widths()

    def update_translations(self, translated_lyrics):
        for item in self.tree.get_children():
            item_data = self.tree.item(item)
            start_time = item_data['values'][0]
            original_lyrics = item_data['values'][1]
            for lyric in translated_lyrics:
                if self.ms_to_min_sec(lyric['startTimeMs']) == start_time and lyric['words'] == original_lyrics:
                    self.tree.set(item, column="Translated Lyrics", value=lyric['translated'])
                    break
        if self.tree.get_children():
            first_item = self.tree.get_children()[0]
            self.tree.set(first_item, column="Translated Lyrics", value=translated_lyrics[0]['translated'])
        self.adjust_column_widths()

    def adjust_column_widths(self):
        min_time_width = 60
        max_original_length = 0
        max_translated_length = 0
        line_count = 0

        for item in self.tree.get_children():
            line_count += 1
            original_length = len(self.tree.item(item)['values'][1])
            translated_length = len(self.tree.item(item)['values'][2])
            if original_length > max_original_length:
                max_original_length = original_length
            if translated_length > max_translated_length:
                max_translated_length = translated_length

        self.root.update_idletasks()
        width = self.tree.winfo_reqwidth()

        orig_length = max_original_length * 15
        trans_length = max_translated_length * 15

        if self.language == "ja":
            orig_length = max_original_length * 23
        if self.language == "ru":
            orig_length = max_original_length * 18
            trans_length = max_translated_length * 19

        width = min_time_width + orig_length + trans_length
        height = line_count * 17 + 100

        current_width = self.root.winfo_width()

        self.tree.column("Time", width=min_time_width, minwidth=min_time_width)
        self.tree.column("Original Lyrics", width=orig_length)
        self.tree.column("Translated Lyrics", width=trans_length)
        self.root.geometry(f"{current_width}x{height}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SpotifyLyricsTranslator()
    app.run()
