#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Spotify Translator setup..."

# Check if Python 3.11 is available
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 is required but not installed."
    echo "💡 Please install it with: brew install python@3.11"
    exit 1
fi

# Check if tkinter is installed
if ! python3.11 -c "import tkinter" &> /dev/null; then
    echo "❌ Python Tkinter is required but not installed."
    echo "💡 Please install it with: brew install python-tk@3.11"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "✨ Starting application..."
python app.py 