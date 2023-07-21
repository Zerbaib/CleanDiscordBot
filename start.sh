#bin/bash

apt install python3-venv -y
apt install python3-pip -y
apt install python-is-python3 -y

python -m venv .venv
source env/bin/activate

git fetch
git pull

pip install -r requirements.txt

python main.py