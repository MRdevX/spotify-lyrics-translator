import PyInstaller.__main__
import os

# Get the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'app.py',
    '--name=SpotifyLyricsTranslator',
    '--onefile',
    '--windowed',
    '--icon=icon.ico',  # You'll need to create/add an icon file
    '--add-data=sv_ttk;sv_ttk',  # Include the sv_ttk theme files
    '--hidden-import=sv_ttk',
    '--hidden-import=deep_translator',
    '--hidden-import=syrics',
    f'--workpath={os.path.join(script_dir, "build")}',
    f'--distpath={os.path.join(script_dir, "dist")}',
    '--clean'
]) 