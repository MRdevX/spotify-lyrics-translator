#!/usr/bin/env python3
"""
Build script for creating macOS app
"""
import os
import subprocess
import shutil
import sys
import platform
import glob

def get_project_root():
    """Get the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous builds...")
    project_root = get_project_root()
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        dir_path = os.path.join(project_root, dir_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    
    # Also clean .pyc files and __pycache__ directories
    for root, dirs, files in os.walk(project_root):
        for d in dirs:
            if d == '__pycache__':
                shutil.rmtree(os.path.join(root, d))
        for f in files:
            if f.endswith('.pyc'):
                os.remove(os.path.join(root, f))

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    project_root = get_project_root()
    try:
        # Ensure pip is up to date
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        
        # Install requirements from file
        requirements_path = os.path.join(project_root, 'requirements.txt')
        print("Installing requirements from requirements.txt...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', requirements_path], check=True)
        
        # Install py2app with specific version
        print("Installing py2app...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'py2app==0.28.6'], check=True)
        
        # Verify critical imports
        print("\nVerifying installations:")
        critical_packages = [
            ('tkinter', 'Tkinter'),
            ('deep_translator', 'Deep Translator'),
            ('syrics', 'Syrics'),
            ('sv_ttk', 'Sun Valley TTK Theme'),
            ('spotipy', 'Spotipy'),
            ('PIL', 'Pillow')
        ]
        
        for package, name in critical_packages:
            try:
                module = __import__(package)
                print(f"✓ {name} successfully imported")
            except ImportError as e:
                print(f"✗ Error: {name} import failed: {e}")
                raise
            
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        raise

def verify_files():
    """Verify all required files exist"""
    project_root = get_project_root()
    required_files = [
        ('src/main.py', 'Main application file'),
        ('src/config/config.json', 'Configuration file'),
        ('assets/app_icon.icns', 'Application icon'),
        ('requirements.txt', 'Requirements file'),
        ('scripts/setup.py', 'Setup configuration')
    ]
    
    missing_files = []
    for file_path, description in required_files:
        full_path = os.path.join(project_root, file_path)
        if not os.path.exists(full_path):
            missing_files.append(f"{description} ({file_path})")
    
    if missing_files:
        print("Error: Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        raise FileNotFoundError("Required files are missing")

def build_app():
    """Build the macOS app"""
    print("Building macOS app...")
    try:
        project_root = get_project_root()
        os.chdir(project_root)  # Change to project root directory
        verify_files()
        
        # Build command for standalone app
        setup_path = os.path.join(project_root, 'scripts/setup.py')
        build_cmd = [
            sys.executable,
            setup_path,
            'py2app',
            '-A',  # Use alias mode for development
            '--packages=tkinter,deep_translator,syrics,sv_ttk,spotipy,PIL'
        ]
        
        # Add architecture flag if on Apple Silicon
        if platform.machine() == 'arm64':
            build_cmd.extend(['--arch=arm64'])
        
        print(f"Running build command: {' '.join(build_cmd)}")
        subprocess.run(build_cmd, check=True)
        
        # Verify the app bundle
        app_path = os.path.join(project_root, 'dist', 'Spotify Lyrics Translator.app')
        if not os.path.exists(app_path):
            raise FileNotFoundError(f"App bundle not found at {app_path}")
        
        print("\nVerifying app bundle contents:")
        critical_paths = [
            'Contents/MacOS/Spotify Lyrics Translator',
            'Contents/Resources/lib/python*/site-packages',
            'Contents/Resources/src/main.py',
            'Contents/Resources/src/config/config.json'
        ]
        
        for path in critical_paths:
            full_path = os.path.join(app_path, path)
            matches = glob.glob(full_path)
            if not matches:
                print(f"✗ Warning: {path} not found in app bundle")
            else:
                print(f"✓ Found {path}")
        
        print("\nBuild completed successfully!")
        print(f"App bundle created at: {os.path.abspath(app_path)}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during build: {e}")
        raise

def verify_environment():
    """Verify the build environment"""
    print("\nVerifying build environment:")
    project_root = get_project_root()
    
    # Check Python version
    python_version = sys.version.split()[0]
    print(f"✓ Python version: {python_version}")
    
    # Check virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        raise EnvironmentError("Please run this script in a virtual environment")
    print("✓ Running in virtual environment")
    
    # Check directory structure
    src_path = os.path.join(project_root, 'src')
    if not os.path.isdir(src_path):
        raise EnvironmentError("Project structure is invalid (src/ directory not found)")
    print("✓ Directory structure verified")

def main():
    """Main build process"""
    try:
        print("\nStarting build process for Spotify Lyrics Translator")
        print("=" * 50)
        
        print("\nSystem Information:")
        print(f"Python version: {sys.version}")
        print(f"Platform: {platform.platform()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Working directory: {os.getcwd()}")
        
        verify_environment()
        clean_build()
        install_requirements()
        build_app()
        
        print("\nBuild process completed successfully!")
        print("You can now move 'dist/Spotify Lyrics Translator.app' to your Applications folder.")
        
    except Exception as e:
        print(f"\nError: Build process failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 