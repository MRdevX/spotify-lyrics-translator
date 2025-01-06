#!/usr/bin/env python3
"""
Version and release management script for Spotify Lyrics Translator
"""
import os
import json
import subprocess
import sys
from datetime import datetime
import re

VERSION_FILE = 'version.json'

def get_current_version():
    """Get the current version from version.json"""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            return json.load(f)
    return {'major': 1, 'minor': 0, 'patch': 0, 'build': 0}

def save_version(version):
    """Save version information to version.json"""
    with open(VERSION_FILE, 'w') as f:
        json.dump(version, f, indent=2)

def get_git_commit_count():
    """Get the total number of commits"""
    try:
        result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'],
                              capture_output=True, text=True, check=True)
        return int(result.stdout.strip())
    except subprocess.CalledProcessError:
        return 0

def get_git_hash():
    """Get the current git hash"""
    try:
        result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'],
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return 'unknown'

def update_version(version_type='patch'):
    """Update version numbers based on type"""
    version = get_current_version()
    
    if version_type == 'major':
        version['major'] += 1
        version['minor'] = 0
        version['patch'] = 0
    elif version_type == 'minor':
        version['minor'] += 1
        version['patch'] = 0
    elif version_type == 'patch':
        version['patch'] += 1
    
    version['build'] = get_git_commit_count()
    version['hash'] = get_git_hash()
    version['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    save_version(version)
    return version

def create_git_tag(version):
    """Create a Git tag for the version"""
    version_str = f"v{version['major']}.{version['minor']}.{version['patch']}"
    try:
        # Create an annotated tag
        subprocess.run(['git', 'tag', '-a', version_str, '-m', f"Release {version_str}"], check=True)
        print(f"Created Git tag: {version_str}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating Git tag: {e}")

def update_app_version(version):
    """Update version in setup.py and other relevant files"""
    version_str = f"{version['major']}.{version['minor']}.{version['patch']}"
    
    # Update setup.py
    with open('setup.py', 'r') as f:
        content = f.read()
    
    # Update version strings in setup.py using regex to handle any existing version
    content = re.sub(
        r"'CFBundleVersion':\s*\"[\d.]+\"",
        f"'CFBundleVersion': \"{version_str}\"",
        content
    )
    content = re.sub(
        r"'CFBundleShortVersionString':\s*\"[\d.]+\"",
        f"'CFBundleShortVersionString': \"{version_str}\"",
        content
    )
    
    with open('setup.py', 'w') as f:
        f.write(content)
    
    print(f"Updated version to {version_str} in setup.py")

def get_commit_messages_since_last_tag():
    """Get commit messages since the last tag"""
    try:
        # Get the last tag
        last_tag = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True, text=True, check=True
        ).stdout.strip()
        
        # Get commit messages since last tag
        commits = subprocess.run(
            ['git', 'log', f'{last_tag}..HEAD', '--pretty=format:%s'],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except subprocess.CalledProcessError:
        # If no tags exist, get all commit messages
        commits = subprocess.run(
            ['git', 'log', '--pretty=format:%s'],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    
    return commits.split('\n') if commits else []

def determine_version_bump(commits):
    """Determine version bump type based on commit messages"""
    for commit in commits:
        if re.search(r'^break|^breaking|^major|BREAKING CHANGE', commit, re.I):
            return 'major'
        elif re.search(r'^feat|^feature|^minor', commit, re.I):
            return 'minor'
    return 'patch'

def main():
    """Main function to handle version updates"""
    # Handle command line arguments
    if len(sys.argv) < 2 or sys.argv[1] == '--auto':
        # Auto-determine version bump from commit messages
        commits = get_commit_messages_since_last_tag()
        version_type = determine_version_bump(commits)
        print(f"Automatically determined version bump: {version_type}")
    else:
        version_type = sys.argv[1].lower()
        if version_type not in ['major', 'minor', 'patch']:
            print("Version type must be 'major', 'minor', 'patch', or '--auto'")
            sys.exit(1)
    
    # Check if working directory is clean (unless in CI)
    if 'CI' not in os.environ:
        result = subprocess.run(['git', 'status', '--porcelain'],
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("Error: Working directory is not clean. Commit or stash changes first.")
            sys.exit(1)
    
    # Update version
    version = update_version(version_type)
    version_str = f"{version['major']}.{version['minor']}.{version['patch']}"
    print(f"Updated version to {version_str} (build {version['build']})")
    
    # Update version in app files
    update_app_version(version)
    
    # Create Git tag if not disabled
    if '--no-tag' not in sys.argv:
        create_git_tag(version)
        print("\nNext steps:")
        print(f"1. Push the new tag: git push origin v{version_str}")
        print("2. Build the app: python build_app.py")
        print(f"3. Create a new release on GitHub with tag v{version_str}")

if __name__ == '__main__':
    main() 