#!/usr/bin/env python3
"""
Build script for creating macOS app
"""
import os
import subprocess
import shutil
import sys
import platform

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous builds...")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        # Ensure pip is up to date
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        
        # Install core dependencies first
        core_deps = [
            'Pillow',
            'beautifulsoup4',
            'certifi',
            'requests',
            'urllib3',
            'charset-normalizer',
            'idna',
            'soupsieve',
            'spotipy',
            'tqdm',
            'tinytag',
            'redis'
        ]
        
        for dep in core_deps:
            print(f"Installing {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', dep], check=True)
        
        # Install requirements from file
        print("Installing requirements from requirements.txt...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        
        # Install py2app last
        print("Installing py2app...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'py2app'], check=True)
        
        # Verify critical imports
        print("\nVerifying installations:")
        try:
            import PIL
            print(f"PIL/Pillow version: {PIL.__version__}")
            print(f"PIL path: {PIL.__file__}")
        except ImportError as e:
            print(f"Warning: PIL import failed: {e}")
            
        try:
            import bs4
            print(f"BeautifulSoup4 version: {bs4.__version__}")
            print(f"BS4 path: {bs4.__file__}")
        except ImportError as e:
            print(f"Warning: BeautifulSoup4 import failed: {e}")
            
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        raise

def build_app():
    """Build the macOS app"""
    print("Building macOS app...")
    try:
        # Build command
        build_cmd = [sys.executable, 'setup.py', 'py2app']
        
        # Add architecture flag if on Apple Silicon
        if platform.machine() == 'arm64':
            build_cmd.append('--arch=arm64')
            
        # Add no-strip flag
        build_cmd.append('--no-strip')
        
        print(f"Running build command: {' '.join(build_cmd)}")
        subprocess.run(build_cmd, check=True)
        print("Build completed successfully")
        
        # Verify the app bundle exists
        app_path = os.path.join('dist', 'Spotify Lyrics Translator.app')
        if os.path.exists(app_path):
            print(f"App bundle created successfully at: {app_path}")
        else:
            print("Warning: App bundle not found in expected location")
            
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        raise

def main():
    """Main build process"""
    try:
        # Print system information
        print("\nSystem Information:")
        print(f"Python version: {sys.version}")
        print(f"Platform: {platform.platform()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Working directory: {os.getcwd()}")
        print()
        
        # Ensure we're in a virtual environment
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("Error: Please run this script in a virtual environment")
            sys.exit(1)

        clean_build()
        install_requirements()
        build_app()
        
        print("\nBuild successful! The app is located in the 'dist' directory.")
        print("You can now move 'dist/Spotify Lyrics Translator.app' to your Applications folder.")
    except Exception as e:
        print(f"\nError during build process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 