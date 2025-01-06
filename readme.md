# 🎵 Spotify Lyrics Translator

![GitHub release (latest by date)](https://img.shields.io/github/v/release/mrdevx/spotify-translator)
![GitHub all releases](https://img.shields.io/github/downloads/mrdevx/spotify-translator/total)
![GitHub](https://img.shields.io/github/license/mrdevx/spotify-translator)
![macOS](https://img.shields.io/badge/macOS-10.13%2B-blue)

<p align="center">
  <img src="assets/app_icon.icns" alt="Spotify Lyrics Translator Logo" width="200">
</p>

> 🌍 Real-time translation of Spotify lyrics in a beautiful, native macOS app

This project is a fork of [spotify-translator](https://github.com/atahanuz/spotify-translator) by [@atahanuz](https://github.com/atahanuz), enhanced with native macOS integration and additional features. Special thanks to Atahan Uz (atahanuz23@gmail.com) for creating the original project that made this possible!

## ✨ Features

- 🔄 Real-time lyrics synchronization with Spotify
- 🌐 Support for multiple translation languages
- 🎨 Modern and native macOS interface
- 🌙 Light/Dark mode support
- ⚡️ Fast and efficient performance
- 🔒 Secure authentication with Spotify

## 🚀 Quick Start

### Installation

#### Option 1: DMG Installer (Recommended)

1. Download the latest `Spotify Lyrics Translator.dmg` from [Releases](https://github.com/mrdevx/spotify-translator/releases)
2. Open the DMG file
3. Drag the app to your Applications folder
4. Launch from Applications or Spotlight

#### Option 2: ZIP Archive

1. Download the latest `Spotify Lyrics Translator.zip`
2. Extract the archive
3. Move the app to Applications folder
4. Launch the app

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

- Seamless macOS integration
- System notifications
- Native window management
- Keyboard shortcuts

## ⚙️ Requirements

- macOS 10.13 or later
- Spotify Premium account
- Active internet connection
- 50MB free disk space
- Python 3.8 or later (for development)

## 🛠️ Development

### Project Structure

```
spotify-translator/
├── assets/                 # Application assets
│   └── app_icon.icns      # App icon
├── scripts/               # Build and utility scripts
│   ├── build_app.py      # Main build script
│   ├── build_dmg.py      # DMG creation orchestrator
│   ├── create_dmg.py     # DMG creation utility
│   └── setup.py          # py2app configuration
├── src/                   # Source code
│   ├── config/           # Configuration files
│   ├── gui/              # GUI components
│   ├── utils/            # Utility modules
│   └── main.py           # Application entry point
├── requirements.txt       # Python dependencies
├── version.json          # Version information
└── README.md             # Project documentation
```

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mrdevx/spotify-translator.git
cd spotify-translator

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Build Process

The project includes several build scripts in the `scripts` directory:

#### Development Build

```bash
# Create development build (alias mode)
python scripts/build_app.py
```

This creates a development build that links to your source files, making it easier to test changes.

#### Production Build

```bash
# Create production build and DMG installer
python scripts/build_dmg.py
```

This script:

1. Cleans previous builds
2. Verifies the environment
3. Installs requirements
4. Creates a standalone app bundle
5. Packages the app into a DMG installer

#### Build Scripts

- `build_app.py`: Creates the macOS application bundle using py2app

  - Verifies development environment
  - Manages dependencies
  - Handles both Intel and Apple Silicon builds
  - Validates the app bundle structure

- `build_dmg.py`: Orchestrates the complete build process

  - Coordinates between build_app.py and create_dmg.py
  - Ensures all steps complete successfully

- `create_dmg.py`: Creates the DMG installer
  - Packages the app for distribution
  - Creates a professional installer with custom background
  - Includes Applications folder shortcut

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

- [@atahanuz](https://github.com/atahanuz) for the original [spotify-translator](https://github.com/atahanuz/spotify-translator) project
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
