import subprocess
import time

# Config files
envFilePath = './.env'
configFilePath = "./config.json"
badWordFilePath = "./bad_words.json"

# Parameters
dataFileLoad = True
utilsLoad = True
multiplicator = 65

# Time gestion
timeSeconds = 1
timeMinutes = timeSeconds * 60
timeHours = timeMinutes * 60
timeDays = timeHours * 24
timeWeeks = timeDays * 7
timeMonths = timeDays * 30
timeYears = timeDays * 365

timeUnits = {
    "s": timeSeconds,
    "m": timeMinutes,
    "h": timeHours,
    "D": timeDays,
    "W": timeWeeks,
    "M": timeMonths,
    "A": timeYears
}

# Language possible
langPossible = [
    "EN",
    "FR",
]

# Data files
dataFilePath = {
    "casino": "./data/casino.json",
    "ranks": "./data/ranks.json",
    "cooldown": "./data/cooldown.json",
    "giveaway": "./data/giveaway.json"
}

# Cogs folder
cogsFolder = "./cogs/"

# Utils cogs
utilsCogPath = {
    "logger": "utils.logger",
    #"automod": "utils.automod",
    "status": "utils.status",
    "voice": "utils.voice"
}

# Repos link
githubLink = "https://github.com"
githubRawLink = "https://raw.githubusercontent.com"
gitBranch = f"/{subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()}"
repoGithub = "/Zerbaib/CleanDiscordBot"

# Version link
localVersionFilePath = "./version.txt"
versionLink = "/version.txt"
onlineVersion = f"{githubRawLink}{repoGithub}{gitBranch}{versionLink}"