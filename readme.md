# Spotify Lyrics Translator

A desktop application that shows real-time translations of Spotify lyrics while you listen to music.

## Features

- Real-time lyrics synchronization with Spotify
- Live translation of lyrics using Google Translate
- Clean and modern user interface
- Lyrics caching for better performance
- Support for multiple translation languages

## Requirements

- Python 3.11
- Tkinter (Python GUI library)
- Spotify account

## Installation

### macOS

1. Install Python 3.11 and Tkinter:

```bash
brew install python@3.11
brew install python-tk@3.11
```

2. Clone the repository and run the application:

```bash
git clone [your-repo-url]
cd spotify-translator
./run.sh
```

The script will automatically:

- Create a virtual environment
- Install dependencies
- Start the application

### Manual Installation

If you prefer manual installation:

1. Create and activate virtual environment:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

## First-time Setup

1. When you first run the application, you'll need to authenticate with Spotify:

   - Click "Open Spotify" in the authentication dialog
   - Log in to Spotify if needed
   - Press F12 to open Developer Tools
   - Go to Application > Cookies > https://spotify.com
   - Copy the value of the `sp_dc` cookie
   - Paste it into the application

2. The application will save your authentication for future use

## Troubleshooting

### Authentication Issues

- Make sure you're logged into Spotify in your browser
- Try logging out and back into Spotify to get a fresh cookie
- Verify you copied the entire `sp_dc` cookie value

### Display Issues

- Ensure Python Tkinter is properly installed
- Try resetting column widths using the right-click menu

## Cache Management

The application caches translated lyrics to improve performance. The cache is stored in `lyrics_cache.pkl` and is limited to 1000 entries.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your License]
