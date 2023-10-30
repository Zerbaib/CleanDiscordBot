@echo off

REM Fetch and pull the latest changes from the Git repository.
git.cmd fetch && git.cmd pull

REM Upgrade pip.
pip.exe install --upgrade pip

REM Install the requirements.
pip.exe install -r requirements.txt

REM Run the main Python script.
python.exe main.py

REM Pause the script so that the user can see the output.
pause