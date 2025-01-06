# Spotify Lyrics Translator

Display translated lyrics of the currently playing Spotify track in real-time, with an easy-to-use interface!

## Features
- Real-time lyrics synchronization with Spotify
- Automatic language detection and translation to English
- Clean, modern interface
- Caching system for faster loading of previously translated songs
- Simple one-click installation

## Installation

### System Requirements

#### macOS
```bash
brew install python-tk
```

#### Ubuntu/Debian
```bash
sudo apt-get install python3-tk
```

#### Fedora
```bash
sudo dnf install python3-tkinter
```

### For Users
1. Download the latest release from the [Releases](https://github.com/yourusername/spotify-lyrics-translator/releases) page
2. Run the SpotifyLyricsTranslator executable
3. Follow the in-app instructions to authenticate with Spotify

### For Developers

1. Clone the repository:
```bash
git clone https://github.com/yourusername/spotify-lyrics-translator.git
cd spotify-lyrics-translator
```

2. Create and activate a virtual environment:

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

## First-Time Setup

1. Launch the application
2. Click the "Open Spotify" button in the authentication dialog
3. Log in to Spotify if needed
4. Press F12 to open Developer Tools
5. Go to Application > Cookies > https://spotify.com
6. Find 'sp_dc' cookie and copy its value
7. Paste the value in the application's login dialog

The app will remember your authentication for future uses.

## Screenshots

<table>
  <tr>
    <td style="text-align: center;">
      <p>Spotify's Native Lyrics Display</p>
      <img src="https://i.imgur.com/7PoYKzL.png" alt="Native lyrics display of Spotify" style="width: 100%;" />
    </td>
    <td style="text-align: center;">
      <p>Translated Lyrics Display on the App</p>
      <img src="https://i.imgur.com/IY6v5y8.png" alt="The app with translation" style="width: 91%;" />
    </td>
  </tr>
</table>

## How It Works

The program uses the Google Translate API to translate lyrics from any language to English. It maintains a cache of the last 1000 translated songs to improve performance. The cache is stored in your user directory and persists between sessions.

## Troubleshooting

### Common Issues

1. **Authentication Error**
   - Make sure you're logged into Spotify in your browser
   - Verify that you copied the correct cookie value
   - Try logging out and back into Spotify

2. **No Lyrics Showing**
   - Ensure the current song has lyrics available on Spotify
   - Check your internet connection

3. **Translation Not Working**
   - Check your internet connection
   - Try restarting the application

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Thanks

Thanks to @akashrchandran for his Spotify Lyrics API which made this app possible: https://github.com/akashrchandran/syrics

## Contact

For bug reports and feature requests, please [open an issue](https://github.com/yourusername/spotify-lyrics-translator/issues) on GitHub.

For other inquiries, you can reach me at atahanuz23@gmail.com.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
