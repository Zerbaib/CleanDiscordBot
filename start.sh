#!/bin/bash

git fetch && git pull
pip3 install --upgrade pip
pip3 install -r requirements.txt

python3 main.py