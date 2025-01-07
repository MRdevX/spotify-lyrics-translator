#!/usr/bin/env python3
"""
Build script for creating macOS and Windows apps
"""
import os
import subprocess
import shutil
import sys
import platform
import glob
from PIL import Image

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
        
        # Install build tools based on platform
        if sys.platform == 'darwin':
            print("Installing py2app...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'py2app==0.28.6'], check=True)
        else:
            print("Installing pyinstaller...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pyinstaller==6.3.0'], check=True)
        
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
        ('requirements.txt', 'Requirements file')
    ]
    
    # Add platform-specific files
    if sys.platform == 'darwin':
        required_files.extend([
            ('assets/app_icon.icns', 'Application icon'),
            ('scripts/setup.py', 'Setup configuration')
        ])
    else:
        required_files.append(('assets/app_icon.ico', 'Application icon'))
    
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

def build_macos_app():
    """Build the macOS app using py2app"""
    print("Building macOS application bundle...")
    try:
        verify_files()
        
        # Build command for production app
        build_cmd = [
            sys.executable,
            'scripts/setup.py',
            'py2app',
            '--packages=tkinter,deep_translator,syrics,sv_ttk,spotipy,PIL'
        ]
        
        print(f"Running build command: {' '.join(build_cmd)}")
        subprocess.run(build_cmd, check=True)
        
        # Verify the app bundle
        app_path = os.path.join('dist', 'Spotify Lyrics Translator.app')
        if not os.path.exists(app_path):
            raise FileNotFoundError(f"App bundle not found at {app_path}")
        
        print("\nVerifying app bundle contents:")
        critical_paths = [
            'Contents/MacOS/Spotify Lyrics Translator',
            'Contents/Resources/lib/python*/site-packages',
            'Contents/Resources/src/main.py',
            'Contents/Resources/src/config/config.json',
            'Contents/Frameworks/Python.framework/Versions/Current/Python'
        ]
        
        for path in critical_paths:
            full_path = os.path.join(app_path, path)
            matches = glob.glob(full_path)
            if not matches:
                print(f"✗ Warning: {path} not found in app bundle")
            else:
                print(f"✓ Found {path}")
        
        # Fix permissions
        subprocess.run(['chmod', '-R', '755', app_path], check=True)
        
        print("\nBuild completed successfully!")
        print(f"App bundle created at: {os.path.abspath(app_path)}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during build: {e}")
        raise

def build_windows_app():
    """Build the Windows app using PyInstaller"""
    print("Building Windows executable...")
    try:
        verify_files()
        project_root = get_project_root()
        
        # Create spec file content
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [os.path.join('{project_root}', 'src', 'main.py')],
    pathex=['{project_root}'],
    binaries=[],
    datas=[
        (os.path.join('{project_root}', 'src', 'config'), 'src/config'),
        (os.path.join('{project_root}', 'assets'), 'assets'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'PIL',
        'PIL._tkinter_finder',
        'deep_translator',
        'syrics',
        'sv_ttk',
        'spotipy',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Spotify Lyrics Translator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('{project_root}', 'assets', 'app_icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Spotify Lyrics Translator',
)
'''
        
        # Write spec file
        with open('spotify_translator.spec', 'w') as f:
            f.write(spec_content)
        
        # Build using PyInstaller
        subprocess.run([
            sys.executable,
            '-m',
            'PyInstaller',
            '--clean',
            '--noconfirm',
            'spotify_translator.spec'
        ], check=True)
        
        print("\nBuild completed successfully!")
        print(f"Executable created at: {os.path.abspath('dist/Spotify Lyrics Translator')}")
        
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
    print(f"Python version: {python_version}")
    
    # Check virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        raise EnvironmentError("Please run this script in a virtual environment")
    print("Virtual environment: OK")
    
    # Check directory structure
    src_path = os.path.join(project_root, 'src')
    if not os.path.isdir(src_path):
        raise EnvironmentError("Project structure is invalid (src/ directory not found)")
    print("Directory structure: OK")

def convert_icon():
    """Convert macOS icon to Windows format if needed"""
    if sys.platform == 'win32':
        try:
            project_root = get_project_root()
            icns_path = os.path.join(project_root, 'assets', 'app_icon.icns')
            ico_path = os.path.join(project_root, 'assets', 'app_icon.ico')
            
            if not os.path.exists(ico_path) and os.path.exists(icns_path):
                print("Converting icon to Windows format...")
                # Convert ICNS to PNG first
                img = Image.open(icns_path)
                png_path = os.path.join(project_root, 'assets', 'temp_icon.png')
                img.save(png_path, 'PNG')
                
                # Convert PNG to ICO
                img = Image.open(png_path)
                icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
                img.save(ico_path, format='ICO', sizes=icon_sizes)
                
                # Clean up temporary file
                os.remove(png_path)
                print("Icon conversion completed")
                
        except Exception as e:
            print(f"Warning: Could not convert icon: {e}")
            print("The application will use a default icon")

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
        
        # Set architecture based on platform
        if sys.platform == 'darwin':
            os.environ['ARCHFLAGS'] = "-arch arm64"
        else:
            os.environ['ARCHFLAGS'] = "-arch x86_64"
            # Set UTF-8 encoding for Windows
            if sys.platform == 'win32':
                sys.stdout.reconfigure(encoding='utf-8')
                sys.stderr.reconfigure(encoding='utf-8')
        
        verify_environment()
        clean_build()
        install_requirements()
        convert_icon()
        
        if sys.platform == 'darwin':
            build_macos_app()
        else:
            build_windows_app()
        
        print("\nBuild process completed successfully!")
        
    except Exception as e:
        print(f"\nError: Build process failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 