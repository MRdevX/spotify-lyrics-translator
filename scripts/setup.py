"""
Setup script for building the macOS app using py2app
"""
import os
import sys
from setuptools import setup

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

APP = [os.path.join(project_root, 'src/main.py')]
DATA_FILES = [
    ('src/config', [os.path.join(project_root, 'src/config/config.json')]),
    ('assets', [os.path.join(project_root, 'assets/app_icon.icns')])
]

OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'CFBundleName': 'Spotify Lyrics Translator',
        'CFBundleDisplayName': 'Spotify Lyrics Translator',
        'CFBundleGetInfoString': 'Translate Spotify lyrics in real-time',
        'CFBundleIdentifier': 'com.mrdevx.spotifylyricsapp',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2024 MrDevX',
        'LSMinimumSystemVersion': '10.10.0'
    },
    'packages': [
        'tkinter',
        'deep_translator',
        'syrics',
        'sv_ttk',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'tqdm',
        'spotipy',
        'redis',
        'bs4',
        'PIL'
    ],
    'includes': [
        'tkinter',
        'tkinter.ttk',
        'PIL',
        'sv_ttk'
    ],
    'iconfile': os.path.join(project_root, 'assets/app_icon.icns'),
    'resources': [os.path.join(project_root, 'src')],
    'site_packages': True,
    'strip': False,
    'semi_standalone': True
}

def main():
    # Change to project root directory
    os.chdir(project_root)
    
    setup(
        name='Spotify Lyrics Translator',
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

if __name__ == '__main__':
    main() 