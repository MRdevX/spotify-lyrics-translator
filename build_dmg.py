#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def build_app():
    print("Building macOS application bundle...")
    subprocess.run([
        'pyinstaller',
        '--name=SpotifyTranslator',
        '--windowed',
        '--onefile',
        '--icon=app_icon.icns',
        '--add-data=app_icon.icns:.',
        'app.py'
    ], check=True)

def create_dmg():
    print("Creating DMG file...")
    app_path = 'dist/SpotifyTranslator.app'
    dmg_path = 'dist/SpotifyTranslator.dmg'
    
    if not os.path.exists(app_path):
        print(f"Error: {app_path} not found!")
        sys.exit(1)
    
    # Create DMG using create-dmg
    subprocess.run([
        'create-dmg',
        '--volname', 'Spotify Translator',
        '--volicon', 'app_icon.icns',
        '--window-pos', '200', '120',
        '--window-size', '800', '400',
        '--icon-size', '100',
        '--icon', 'SpotifyTranslator.app', '200', '200',
        '--hide-extension', 'SpotifyTranslator.app',
        '--app-drop-link', '600', '200',
        dmg_path,
        app_path
    ], check=True)

if __name__ == '__main__':
    build_app()
    create_dmg() 