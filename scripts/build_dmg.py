#!/usr/bin/env python3
"""
Script to build the app and create a DMG installer
"""
import os
import sys
import subprocess
from pathlib import Path

def get_project_root():
    """Get the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def build_app():
    """Build the macOS application bundle"""
    print("Building macOS application bundle...")
    project_root = get_project_root()
    os.chdir(project_root)
    
    # Run the build_app.py script
    build_script = os.path.join(project_root, 'scripts/build_app.py')
    subprocess.run([sys.executable, build_script], check=True)

def create_dmg():
    """Create DMG file"""
    print("Creating DMG file...")
    project_root = get_project_root()
    os.chdir(project_root)
    
    # Run the create_dmg.py script
    create_dmg_script = os.path.join(project_root, 'scripts/create_dmg.py')
    subprocess.run([sys.executable, create_dmg_script], check=True)

def main():
    """Main build process"""
    try:
        print("\nStarting build and DMG creation process...")
        print("=" * 50)
        
        # Build the app
        build_app()
        
        # Create the DMG
        create_dmg()
        
        print("\nBuild and DMG creation completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"\nError during build process: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 