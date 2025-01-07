# 🎵 Spotify Lyrics Translator

![GitHub release (latest by date)](https://img.shields.io/github/v/release/mrdevx/spotify-translator)
![GitHub all releases](https://img.shields.io/github/downloads/mrdevx/spotify-translator/total)
![GitHub](https://img.shields.io/github/license/mrdevx/spotify-translator)
![macOS](https://img.shields.io/badge/macOS-10.13%2B-blue)
![Windows](https://img.shields.io/badge/Windows-10%2B-blue)

<p align="center">
  <img src="assets/app_icon.png" alt="Spotify Lyrics Translator Logo" width="200">
</p>

> 🌍 A powerful desktop application that provides real-time translation of Spotify lyrics while you listen to music. Experience your favorite songs in any language with synchronized translations, beautiful interface, and seamless integration with Spotify.

## ✨ Features

- 🔄 Real-time lyrics synchronization with Spotify
- 🌐 Support for multiple translation languages
- 🎨 Modern and native interface for both macOS and Windows
- 🌙 Light/Dark mode support
- ⚡️ Fast and efficient performance
- 🔒 Secure authentication with Spotify
- 💾 Smart caching system for faster translations
- 🖥️ Cross-platform support (macOS & Windows)

## 🚀 Quick Start

### Installation

#### macOS

##### Option 1: DMG Installer (Recommended)

1. Download the latest `Spotify Lyrics Translator.dmg` from [Releases](https://github.com/mrdevx/spotify-translator/releases)
2. Open the DMG file
3. Drag the app to your Applications folder
4. Launch from Applications or Spotlight

##### Option 2: ZIP Archive

1. Download the latest `Spotify Lyrics Translator-macOS.zip`
2. Extract the archive
3. Move the app to Applications folder
4. Launch the app

#### Windows

1. Download the latest `Spotify Lyrics Translator-Windows.zip`
2. Extract the archive
3. Run `Spotify Lyrics Translator.exe`

### First Run Setup

1. Launch Spotify and play any song
2. Open Spotify Lyrics Translator
3. Log in to your Spotify account when prompted
4. Select your preferred translation language
5. Enjoy real-time translated lyrics!

## 🌟 Key Features Explained

### Real-time Lyrics Sync

The app automatically detects the currently playing song on Spotify and fetches its lyrics in real-time, ensuring perfect synchronization with the music.

### Translation Engine

Powered by advanced translation APIs, supporting:

- 100+ languages
- Accurate translations
- Context-aware processing
- Fast response times

### Native Experience

- Seamless system integration
- System notifications
- Native window management
- Keyboard shortcuts

## ⚙️ Requirements

### macOS

- macOS 10.13 or later
- Apple Silicon or Intel Mac
- Spotify Premium account
- Active internet connection
- 50MB free disk space

### Windows

- Windows 10 or later
- Spotify Premium account
- Active internet connection
- 50MB free disk space

## 🛠️ Development

### Project Structure

```
spotify-translator/
├── .github/                # GitHub configuration
│   └── workflows/         # GitHub Actions workflows
├── assets/                # Application assets
│   └── app_icon.png      # App icon
├── scripts/              # Build and utility scripts
│   ├── build_app.py     # Main build script
│   ├── build_dmg.py     # DMG creation orchestrator
│   ├── create_dmg.py    # DMG creation utility
│   └── setup.py         # py2app configuration
├── src/                  # Source code
│   ├── config/          # Configuration files
│   ├── gui/             # GUI components
│   ├── utils/           # Utility modules
│   └── main.py          # Application entry point
├── requirements.txt      # Python dependencies
├── version.json         # Version information
└── README.md            # Project documentation
```

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mrdevx/spotify-translator.git
cd spotify-translator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Build Process

The project includes several build scripts in the `scripts` directory:

#### Development Build

```bash
# Create development build
python scripts/build_app.py
```

This creates a development build that links to your source files, making it easier to test changes.

#### Production Build

```bash
# Create production build and installer
python scripts/build_dmg.py  # For macOS
python scripts/build_app.py  # For Windows
```

This script:

1. Cleans previous builds
2. Verifies the environment
3. Installs requirements
4. Creates a standalone app bundle
5. Packages the app into an installer

### Release Process

The project uses GitHub Actions for automated builds and releases. The process is managed by the version manager script in `scripts/version_manager.py`.

To create a new release:

```bash
# Update version and create release (choose one):
python scripts/version_manager.py major  # For major version updates (x.0.0)
python scripts/version_manager.py minor  # For minor version updates (0.x.0)
python scripts/version_manager.py patch  # For patch updates (0.0.x)

# Add release notes:
python scripts/version_manager.py patch --notes "Fixed bug in lyrics display"

# Test what would happen (dry run):
python scripts/version_manager.py patch --dry-run
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Commit Convention

We follow the conventional commits specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build process or auxiliary tool changes

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [spotify-translator](https://github.com/atahanuz/spotify-translator) by [@atahanuz](https://github.com/atahanuz)
- [Spotify](https://spotify.com) for their amazing platform
- [Syrics](https://github.com/akashrchandran/syrics) for lyrics fetching
- [Deep Translator](https://github.com/nidhaloff/deep-translator) for translations
- [Sun Valley TTK Theme](https://github.com/rdbende/Sun-Valley-ttk-theme) for the beautiful UI

## 📬 Contact

Mahdi Rashidi - [@mrdevx](https://github.com/mrdevx)

Project Link: [https://github.com/mrdevx/spotify-translator](https://github.com/mrdevx/spotify-translator)

---

<p align="center">
Made with ❤️ for music lovers
</p>
