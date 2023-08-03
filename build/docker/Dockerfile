FROM ghcr.io/parkervcp/yolks:python_3.11

WORKDIR /bot

COPY . /bot

CMD ["sh", "-c", "if [ ! -d \"bot\" ]; then git clone https://github.com/Zerbaib/CleanDiscordBot.git bot && cd bot && pip install --upgrade pip && pip install -r requirements.txt && python main.py; else cd bot && git fetch && git pull && pip install --upgrade pip && pip install -r requirements.txt && python main.py; fi"]
