#!/bin/bash

# Check if git is installed, install if not
if ! command -v git &> /dev/null; then
    echo "Git not found. Installing..."
    sudo apt update
    sudo apt install -y git
fi

# Check if python3 is installed, install if not
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3
fi

# Check if python3-venv is installed, install if not
if ! command -v python3 -m  venv &> /dev/null; then
    echo "Python3-venv not found. Installing..."
    sudo apt update
    sudo apt install -y python3-venv
fi

# Check if pip3 is installed, install if not
if ! command -v pip3 &> /dev/null; then
    echo "Pip3 not found. Installing..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Activate virtual environment if it exists, otherwise create and activate it
if [ -d ".venv" ]; then
    echo "Activating existing virtual environment..."
    source .venv/bin/activate
else
    echo "Creating and activating new virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Fetch latest changes from git repository
echo "Fetching latest changes from git..."
git fetch && git pull

# Upgrade pip and install required packages
echo "Upgrading pip and installing required packages..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Run the main.py script
echo "Running main.py..."
python3 main.py