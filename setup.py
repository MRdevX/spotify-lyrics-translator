"""
Setup script for building macOS app using py2app
"""
from setuptools import setup

APP = ['app.py']
DATA_FILES = ['config.json']
OPTIONS = {
    'argv_emulation': False,
    'packages': ['tkinter', 'deep_translator', 'syrics', 'sv_ttk'],
    'includes': ['webbrowser', 'json', 'pickle', 'threading', 'concurrent.futures'],
    'iconfile': 'app_icon.icns',
    'plist': {
        'CFBundleName': 'Spotify Lyrics Translator',
        'CFBundleDisplayName': 'Spotify Lyrics Translator',
        'CFBundleIdentifier': 'com.spotifytranslator.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.10',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'LSApplicationCategoryType': 'public.app-category.music',
        'NSAppleEventsUsageDescription': 'This app needs to access Spotify to translate lyrics.',
    }
}

setup(
    name='Spotify Lyrics Translator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 