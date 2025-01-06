import PyInstaller.__main__
import os
import sys
from pathlib import Path
import shutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def clean_build_directories():
    """Clean up build directories before building"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                logger.info(f"Cleaned {dir_name} directory")
            except Exception as e:
                logger.error(f"Error cleaning {dir_name}: {e}")

def build_application():
    """Build the application using PyInstaller"""
    try:
        # Get the directory containing this script
        script_dir = Path(__file__).parent.absolute()
        
        # Clean previous builds
        clean_build_directories()
        
        # Ensure assets directory exists
        assets_dir = script_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        
        # Default icon path
        icon_path = assets_dir / 'icon.ico'
        
        # PyInstaller configuration
        PyInstaller.__main__.run([
            'app.py',
            '--name=SpotifyLyricsTranslator',
            '--onefile',
            '--windowed',
            f'--icon={icon_path}',
            '--add-data=sv_ttk;sv_ttk',
            '--hidden-import=sv_ttk',
            '--hidden-import=deep_translator',
            '--hidden-import=syrics',
            f'--workpath={script_dir / "build"}',
            f'--distpath={script_dir / "dist"}',
            '--clean',
            '--log-level=INFO'
        ])
        
        logger.info("Build completed successfully!")
        
    except Exception as e:
        logger.error(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_application() 