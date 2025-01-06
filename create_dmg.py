#!/usr/bin/env python3
"""
Script to create DMG file for Spotify Lyrics Translator
"""
import os
import subprocess
import json
import shutil

def get_version():
    """Get current version from version.json"""
    with open('version.json', 'r') as f:
        version = json.load(f)
        return f"{version['major']}.{version['minor']}.{version['patch']}"

def create_dmg():
    """Create DMG file from the app bundle"""
    version = get_version()
    app_name = "Spotify Lyrics Translator"
    dmg_name = f"{app_name}-{version}"
    
    # Ensure we're in the project root
    if not os.path.exists('dist'):
        print("Error: 'dist' directory not found")
        return False
    
    if not os.path.exists(f'dist/{app_name}.app'):
        print(f"Error: '{app_name}.app' not found in dist directory")
        return False
        
    print(f"Creating DMG for {app_name} version {version}...")
    
    try:
        # Clean up any existing temporary files
        temp_dir = 'dist/dmg_temp'
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # Copy app bundle to temporary directory
        shutil.copytree(
            f'dist/{app_name}.app',
            f'{temp_dir}/{app_name}.app',
            symlinks=True
        )
        
        # Create symbolic link to Applications folder
        os.symlink('/Applications', f'{temp_dir}/Applications')
        
        # Remove any existing DMG files
        dmg_path = f'dist/{dmg_name}.dmg'
        temp_dmg_path = f'dist/{dmg_name}_temp.dmg'
        if os.path.exists(dmg_path):
            os.remove(dmg_path)
        if os.path.exists(temp_dmg_path):
            os.remove(temp_dmg_path)
        
        # Create temporary DMG
        subprocess.run([
            'hdiutil', 'create',
            '-volname', app_name,
            '-srcfolder', temp_dir,
            '-ov',
            '-format', 'UDRW',
            temp_dmg_path
        ], check=True)
        
        # Convert to compressed DMG
        subprocess.run([
            'hdiutil', 'convert',
            temp_dmg_path,
            '-format', 'UDZO',
            '-o', dmg_path
        ], check=True)
        
        print(f"Successfully created {dmg_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating DMG: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        # Clean up temporary files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if os.path.exists(temp_dmg_path):
            os.remove(temp_dmg_path)

if __name__ == '__main__':
    create_dmg() 