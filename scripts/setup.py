"""
Setup script for building the macOS app using py2app
"""
import os
import sys
import platform
import json
from setuptools import setup

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Get Python version info
python_version = platform.python_version()
python_short_version = '.'.join(python_version.split('.')[:2])

# Determine Python framework paths based on architecture
framework_base = '/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11' if platform.machine() == 'arm64' else '/usr/local/opt/python@3.11/Frameworks/Python.framework/Versions/3.11'

APP = [os.path.join(project_root, 'src/main.py')]
DATA_FILES = [
    ('src/config', [os.path.join(project_root, 'src/config/config.json')]),
    ('assets', [os.path.join(project_root, 'assets/app_icon.icns')]),
    ('', [os.path.join(project_root, 'version.json')])
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
        'NSHumanReadableCopyright': '© 2025 MrDevX',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.music',
        'CFBundleDocumentTypes': [],
        'CFBundleTypeIconFiles': [],
        'NSRequiresAquaSystemAppearance': False,
        'PyRuntimeLocations': [
            '@executable_path/../Frameworks/Python.framework/Versions/Current/Python',
            f'{framework_base}/Python',
            f'/Library/Frameworks/Python.framework/Versions/{python_short_version}/Python',
            '/usr/local/Frameworks/Python.framework/Python',
        ],
        'PyOptions': {
            'alias': False,
            'argv_emulation': False,
            'site_packages': True,
            'includes': ['pkg_resources.py2_warn']
        }
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
        'PIL'
    ],
    'includes': [
        'tkinter.ttk',
        'PIL',
        'sv_ttk'
    ],
    'excludes': [
        'matplotlib',
        'numpy',
        'scipy',
        'pandas'
    ],
    'iconfile': os.path.join(project_root, 'assets/app_icon.icns'),
    'resources': [os.path.join(project_root, 'src')],
    'frameworks': [f'{framework_base}/Python'],
    'site_packages': True,
    'strip': False,
    'semi_standalone': False,
    'arch': platform.machine()
}

def main():
    """Main setup function."""
    # Change to project root directory
    os.chdir(project_root)
    
    # Read version from version.json
    try:
        with open('version.json', 'r') as f:
            version_data = json.load(f)
            version = f"{version_data['major']}.{version_data['minor']}.{version_data['patch']}"
    except Exception as e:
        print(f"Warning: Could not read version from version.json: {e}")
        version = "1.0.0"
    
    # Update plist version
    OPTIONS['plist'].update({
        'CFBundleVersion': version,
        'CFBundleShortVersionString': version,
    })
    
    setup(
        name='Spotify Lyrics Translator',
        version=version,
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app>=0.28.6'],
        install_requires=[
            'deep_translator',
            'syrics',
            'sv_ttk',
            'Pillow',
            'requests',
            'urllib3',
            'certifi',
            'charset_normalizer',
            'idna'
        ],
    )

if __name__ == '__main__':
    main() 