#!/usr/bin/env python3
"""
Version Manager Script for Spotify Lyrics Translator
Handles version updates and release preparation
"""
import os
import json
import sys
import argparse
from datetime import datetime
import subprocess
from typing import Dict, Tuple, Optional

def get_project_root() -> str:
    """Get the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_version() -> Dict:
    """Load current version information from version.json"""
    version_file = os.path.join(get_project_root(), 'version.json')
    try:
        with open(version_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: version.json not found at {version_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: version.json is not valid JSON")
        sys.exit(1)

def save_version(version_data: Dict) -> None:
    """Save version information to version.json"""
    version_file = os.path.join(get_project_root(), 'version.json')
    try:
        with open(version_file, 'w') as f:
            json.dump(version_data, f, indent=4)
    except Exception as e:
        print(f"Error saving version.json: {e}")
        sys.exit(1)

def get_current_version() -> Tuple[int, int, int]:
    """Get current version numbers"""
    version_data = load_version()
    return (
        version_data['major'],
        version_data['minor'],
        version_data['patch']
    )

def update_version(version_type: str, notes: Optional[str] = None) -> None:
    """Update version numbers based on type (major, minor, patch)"""
    version_data = load_version()
    major, minor, patch = get_current_version()
    
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'patch':
        patch += 1
    else:
        print(f"Invalid version type: {version_type}")
        sys.exit(1)
    
    version_data.update({
        'major': major,
        'minor': minor,
        'patch': patch,
        'build': version_data.get('build', 0) + 1,
        'release_date': datetime.now().strftime('%Y-%m-%d'),
        'release_notes': notes or 'No release notes provided'
    })
    
    save_version(version_data)
    print(f"\nVersion updated to v{major}.{minor}.{patch}")
    return version_data

def verify_git_status() -> bool:
    """Verify git status is clean"""
    try:
        # Check if we're in a git repository
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                     check=True, capture_output=True)
        
        # Check for uncommitted changes
        result = subprocess.run(['git', 'status', '--porcelain'],
                              check=True, capture_output=True, text=True)
        
        if result.stdout.strip():
            print("\nError: You have uncommitted changes. Please commit or stash them first.")
            print("\nUncommitted changes:")
            print(result.stdout)
            return False
            
        return True
        
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git is not installed")
        return False

def create_release(version_data: Dict) -> None:
    """Create a new release"""
    version = f"v{version_data['major']}.{version_data['minor']}.{version_data['patch']}"
    
    try:
        # Create and push tag
        tag_message = f"Release {version}\n\n{version_data['release_notes']}"
        subprocess.run(['git', 'tag', '-a', version, '-m', tag_message], check=True)
        subprocess.run(['git', 'push', 'origin', version], check=True)
        
        print(f"\nCreated and pushed tag: {version}")
        print("GitHub Actions workflow will now:")
        print("1. Build the application")
        print("2. Create the DMG installer")
        print("3. Create a GitHub release")
        print("4. Upload the assets")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating release: {e}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Version Manager for Spotify Lyrics Translator')
    parser.add_argument('action', choices=['major', 'minor', 'patch'],
                       help='Type of version update')
    parser.add_argument('--notes', '-n', help='Release notes')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    print("\nSpotify Lyrics Translator - Version Manager")
    print("=" * 50)
    
    # Show current version
    current = get_current_version()
    print(f"\nCurrent version: v{current[0]}.{current[1]}.{current[2]}")
    
    if args.dry_run:
        print("\nDry run - no changes will be made")
        return
    
    # Verify git status
    if not verify_git_status():
        return
    
    # Update version
    version_data = update_version(args.action, args.notes)
    
    # Commit version update
    try:
        version = f"v{version_data['major']}.{version_data['minor']}.{version_data['patch']}"
        subprocess.run(['git', 'add', 'version.json'], check=True)
        subprocess.run(['git', 'commit', '-m', f"chore: prepare release {version}"], check=True)
        subprocess.run(['git', 'push'], check=True)
        
        print("\nCommitted and pushed version update")
        
        # Create release
        create_release(version_data)
        
    except subprocess.CalledProcessError as e:
        print(f"Error during release process: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 