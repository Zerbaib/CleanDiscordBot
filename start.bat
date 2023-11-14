@echo off

REM Fetch and pull the latest changes from the Git repository.
git.exe fetch && git.exe pull

REM Create and active the env
python -m venv .venv
.venv\Scripts\activate.bat

REM Upgrade pip.
pip.exe install --upgrade pip

REM Install the requirements.
pip.exe install -r requirements.txt

REM Run the main Python script.
python.exe main.py

REM Pause the script so that the user can see the output.
pause