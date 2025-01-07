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
from typing import Dict, Tuple, Optional, List

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

def get_commit_history(since_tag: Optional[str] = None) -> List[Dict[str, str]]:
    """Get commit history with conventional commit parsing."""
    try:
        # Get the last tag if not provided
        if not since_tag:
            result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'],
                                 capture_output=True, text=True)
            if result.returncode == 0:
                since_tag = result.stdout.strip()
            else:
                # If no tags exist, get all commits
                since_tag = ''

        # Get commits since the last tag
        cmd = ['git', 'log', '--pretty=format:%s|%h|%an|%ad', '--date=short']
        if since_tag:
            cmd.append(f'{since_tag}..HEAD')
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits = []
        
        for line in result.stdout.split('\n'):
            if not line:
                continue
            
            message, hash_id, author, date = line.split('|')
            
            # Parse conventional commit format
            commit_type = 'other'
            scope = None
            description = message
            
            if ':' in message:
                type_part, desc_part = message.split(':', 1)
                if '(' in type_part and ')' in type_part:
                    commit_type, scope = type_part.split('(', 1)
                    scope = scope.rstrip(')')
                else:
                    commit_type = type_part
                description = desc_part.strip()
                
            commits.append({
                'type': commit_type.lower(),
                'scope': scope,
                'description': description,
                'hash': hash_id,
                'author': author,
                'date': date
            })
        
        return commits
    
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit history: {e}")
        return []

def generate_changelog(commits: List[Dict[str, str]]) -> str:
    """Generate a formatted changelog from commits."""
    type_emojis = {
        'feat': '✨',
        'fix': '🐛',
        'docs': '📚',
        'style': '💎',
        'refactor': '♻️',
        'perf': '🚀',
        'test': '🧪',
        'build': '🛠️',
        'ci': '⚙️',
        'chore': '🔧',
        'revert': '⏪'
    }
    
    sections = {
        'feat': '### ✨ New Features',
        'fix': '### 🐛 Bug Fixes',
        'docs': '### 📚 Documentation',
        'style': '### 💎 Styles',
        'refactor': '### ♻️ Code Refactoring',
        'perf': '### 🚀 Performance Improvements',
        'test': '### 🧪 Tests',
        'build': '### 🛠️ Build System',
        'ci': '### ⚙️ CI/CD',
        'chore': '### 🔧 Chores',
        'revert': '### ⏪ Reverts'
    }
    
    changes = {}
    for commit in commits:
        commit_type = commit['type']
        if commit_type not in changes:
            changes[commit_type] = []
        
        # Format the commit line
        emoji = type_emojis.get(commit_type, '🔹')
        scope = f"({commit['scope']}) " if commit['scope'] else ""
        description = commit['description']
        hash_id = commit['hash']
        
        commit_line = f"- {emoji} {scope}{description} ({hash_id})"
        changes[commit_type].append(commit_line)
    
    # Build the changelog
    changelog = []
    for commit_type, section_title in sections.items():
        if commit_type in changes and changes[commit_type]:
            changelog.append(section_title)
            changelog.extend(changes[commit_type])
            changelog.append('')  # Empty line between sections
    
    # Add other changes if any
    other_changes = changes.get('other', [])
    if other_changes:
        changelog.append('### 🔹 Other Changes')
        changelog.extend(other_changes)
    
    return '\n'.join(changelog)

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
    
    # Generate changelog from commits
    commits = get_commit_history()
    changelog = generate_changelog(commits)
    
    version_data.update({
        'major': major,
        'minor': minor,
        'patch': patch,
        'build': version_data.get('build', 0) + 1,
        'release_date': datetime.now().strftime('%Y-%m-%d'),
        'release_notes': notes or changelog or 'No release notes provided',
        'changelog': changelog
    })
    
    save_version(version_data)
    print(f"\nVersion updated to v{major}.{minor}.{patch}")
    if changelog:
        print("\nChangelog:")
        print(changelog)
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
        # Create release body with changelog
        release_body = f"""# Spotify Lyrics Translator {version}

## What's Changed

{version_data.get('changelog', 'No changes recorded')}

## Installation

### macOS

#### Option 1: DMG Installer (Recommended)
1. Download `Spotify Lyrics Translator.dmg`
2. Open the DMG file
3. Drag the app to your Applications folder
4. Launch from Applications or Spotlight

#### Option 2: Direct App
1. Download `Spotify Lyrics Translator-macOS.zip`
2. Extract the archive
3. Move to Applications folder
4. Launch the app

### Windows

1. Download `Spotify Lyrics Translator-Windows.zip`
2. Extract the archive
3. Run `Spotify Lyrics Translator.exe`

## System Requirements

### macOS
- macOS 10.13 or later
- Apple Silicon or Intel Mac
- Spotify Premium account
- Active internet connection

### Windows
- Windows 10 or later (64-bit)
- Spotify Premium account
- Active internet connection
"""
        
        # Create and push tag
        tag_message = f"Release {version}\n\n{version_data.get('changelog', 'No changes recorded')}"
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
        commits = get_commit_history()
        changelog = generate_changelog(commits)
        if changelog:
            print("\nChangelog preview:")
            print(changelog)
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