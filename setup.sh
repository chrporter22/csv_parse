#!/usr/bin/env bash

# Exit immediately on error
set -e

echo "Starting setup..."

# Check for Homebrew and install if missing
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew already installed."
fi

# Update Homebrew
echo "Updating Homebrew..."
brew update

# Install Python 3 if missing
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    brew install python
else
    echo "Python 3 already installed."
fi

# Ensure pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip..."
    brew install python-pip
else
    echo "pip already installed."
fi

# Create virtual environment
echo "Creating virtual environment (.venv)..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing requirements.txt..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping."
fi

# Run main.py if it exists
if [ -f "main.py" ]; then
    echo "Running main.py..."
    python main.py
else
    echo "No main.py found. Skipping execution."
fi
