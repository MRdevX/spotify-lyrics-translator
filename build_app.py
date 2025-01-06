#!/usr/bin/env python3
"""
Build script for creating macOS app
"""
import os
import subprocess
import shutil

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
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
    subprocess.run(['pip', 'install', 'py2app'], check=True)

def build_app():
    """Build the macOS app"""
    print("Building macOS app...")
    # First do a test build
    subprocess.run(['python', 'setup.py', 'py2app', '-A'], check=True)
    print("Test build completed successfully")
    
    # Clean and do the final build
    clean_build()
    subprocess.run(['python', 'setup.py', 'py2app'], check=True)
    print("Final build completed successfully")

def main():
    """Main build process"""
    try:
        clean_build()
        install_requirements()
        build_app()
        print("\nBuild successful! The app is located in the 'dist' directory.")
        print("You can now move 'dist/Spotify Lyrics Translator.app' to your Applications folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nError during build process: {e}")
        exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    main() 