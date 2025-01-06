"""
Setup script for building macOS app using py2app
"""
from setuptools import setup

APP = ['app.py']
DATA_FILES = ['config.json', 'lyrics_cache.pkl']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app_icon.icns',
    'plist': {
        'CFBundleName': 'Spotify Lyrics Translator',
        'CFBundleDisplayName': 'Spotify Lyrics Translator',
        'CFBundleGetInfoString': "Translate Spotify lyrics in real-time",
        'CFBundleIdentifier': "com.mrdevx.spotifytranslator",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2024 Mahdi Rashidi, All Rights Reserved",
        'NSHighResolutionCapable': True,
    },
    'packages': ['tkinter', 'deep_translator', 'syrics', 'sv_ttk'],
}

setup(
    name='Spotify Lyrics Translator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 