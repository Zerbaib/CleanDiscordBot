#!/bin/bash

if [ ! -d "bot" ]; then
    git clone https://github.com/Zerbaib/CleanDiscordBot.git bot
    cd bot
    git checkout main
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python main.py
else
    cd bot
    source .venv/bin/activate
    git checkout main
    git fetch
    git pull
    pip install --upgrade pip
    pip install -r requirements.txt
    python main.py
fi