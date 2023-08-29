if [ ! -d "bot" ]; then
    git clone https://github.com/Zerbaib/CleanDiscordBot.git bot
    cd bot
    git checkout main
    pip install --upgrade pip
    pip install -r requirements.txt
    python main.py
else
    cd bot
    git checkout main
    git fetch
    git pull
    pip install --upgrade pip
    pip install -r requirements.txt
    python main.py
fi
