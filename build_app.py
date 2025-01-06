#!/usr/bin/env python3
"""
Build script for creating macOS app
"""
import os
import subprocess
import shutil
import sys

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
        # Install requirements
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        # Install py2app
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'py2app'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        raise

def build_app():
    """Build the macOS app"""
    print("Building macOS app...")
    try:
        # Do the final build directly
        subprocess.run([sys.executable, 'setup.py', 'py2app', '--no-strip'], check=True)
        print("Build completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        raise

def main():
    """Main build process"""
    try:
        # Ensure we're in a virtual environment
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("Error: Please run this script in a virtual environment")
            sys.exit(1)

        print(f"Using Python: {sys.executable}")
        print(f"Python version: {sys.version}")
        
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