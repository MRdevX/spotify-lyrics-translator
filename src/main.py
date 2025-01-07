"""Spotify Lyrics Translator - Main entry point."""

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.gui.app import SpotifyLyricsTranslator

def main():
    if not (sys.version_info.major == 3 and sys.version_info.minor == 11):
        print("Error: Python 3.11 is required.")
        sys.exit(1)

    try:
        app = SpotifyLyricsTranslator()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 