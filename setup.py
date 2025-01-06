"""
Setup script for building macOS app using py2app
"""
from setuptools import setup

APP = ['app.py']
DATA_FILES = []

OPTIONS = {
    'argv_emulation': False,
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
        'LSMinimumSystemVersion': '10.13',
    },
    'packages': [
        'tkinter',
        'deep_translator',
        'syrics',
        'sv_ttk',
        'certifi',
        'requests',
        'urllib3',
        'charset_normalizer',
        'idna',
        'bs4',
        'soupsieve',
        'spotipy',
        'tqdm',
        'tinytag',
        'redis',
        'PIL'
    ],
    'includes': [
        'tkinter.ttk',
        'json',
        'threading',
        'pickle',
        'webbrowser',
        'os',
        'sys',
        'PIL._tkinter_finder',
        'bs4.builder',
        'PIL.Image'
    ],
    'excludes': [
        'matplotlib',
        'numpy',
        'pandas',
        'scipy'
    ],
    'frameworks': [],
    'resources': [],
    'site_packages': True,
    'strip': False,
    'optimize': 0,
    'semi_standalone': True,
    'alias': False,
    'use_faulthandler': True,
    'arch': 'arm64',
    'prefer_ppc': False
}

setup(
    name='Spotify Lyrics Translator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 