"""
Spotify Lyrics Translator - Main entry point.

This module serves as the entry point for the Spotify Lyrics Translator application.
It initializes and starts the main application window.

Author: Mahdi Rashidi
Email: m8rashidi@gmail.com
"""

import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.gui.app import SpotifyLyricsTranslator

def main():
    """Main entry point of the application."""
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
        app = SpotifyLyricsTranslator()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 