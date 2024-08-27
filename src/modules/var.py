import subprocess



class Folders:
    def __init__(self):
        self.src = "./src/"
        self.config = "./config/"
        self.data = "./data/"
        self.log = "./logs/"
        self.cogs = f"{self.src}cogs/"

class Files:
    def __init__(self):
        self.env = f"{folders.config}.env"
        self.config = f"{folders.config}config.json"
        self.badWord = f"{folders.config}bad_words.json"
        self.datebase = f"{folders.data}data.db"
        self.dataFilePath = {
            "giveaway": f"{folders.data}giveaway.json"
            }

class Color:
    def __init__(self):
        self.reset = "\033[0m"
        self.green = f"{self.reset}\033[32m"
        self.red = f"{self.reset}\033[31m"
        self.orange = f"{self.reset}\033[33m"
        self.blue = f"{self.reset}\033[34m"

class Parameters:
    def __init__(self):
        self.dataFileLoad = True
        self.multiplicator = 70
        self.minXpIncrement = 1
        self.maxXpIncrement = 5

class Time:
    def __init__(self):
        self.seconds = 1
        self.minutes = self.seconds * 60
        self.hours = self.minutes * 60
        self.days = self.hours * 24
        self.weeks = self.days * 7
        self.months = self.days * 30
        self.years = self.days * 365

        self.cooldown = self.hours * 2

        self.units = {
            "s": self.seconds,
            "m": self.minutes,
            "h": self.hours,
            "D": self.days,
            "W": self.weeks,
            "M": self.months,
            "A": self.years
        }



time = Time()
color = Color()
folders = Folders()
files = Files()
parameters = Parameters()

# Language possible
langPossible = [
    "EN",
    "FR",
]

# Cogs folder
cogsFolder = f"{folders.src}cogs/"

# Repos link
githubLink = "https://github.com"
githubRawLink = "https://raw.githubusercontent.com"
gitBranch = f"/{subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()}"
repoGithub = "/Zerbaib/CleanDiscordBot"

# Version link
localVersionFilePath = "./version.txt"
versionLink = "/version.txt"
onlineVersion = f"{githubRawLink}{repoGithub}{gitBranch}{versionLink}"
