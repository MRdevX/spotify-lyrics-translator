"""
Setup script for building the macOS app using py2app
"""
from setuptools import setup

APP = ['src/main.py']
DATA_FILES = [
    ('src/config', ['src/config/config.json']),
    ('assets', ['assets/app_icon.icns'])
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
        'LSMinimumSystemVersion': '10.10.0',
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
    'iconfile': 'assets/app_icon.icns',
    'resources': ['src']
}

setup(
    name='Spotify Lyrics Translator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 