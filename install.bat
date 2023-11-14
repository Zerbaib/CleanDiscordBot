@echo off

REM Clone the CleanDiscordBot repository from GitHub.
git.exe clone https://github.com/Zerbaib/CleanDiscordBot.git

REM Install the requirements.
pip.exe install -r CleanDiscordBot/requirements.txt

REM Pause the script so that the user can see the output.
pause