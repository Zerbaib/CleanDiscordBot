import os
from datetime import datetime

from modules.var import *

timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
log_file = os.path.join(folders.log, f"{timestamp}.log")

def get_next_log_file():
    if not os.path.exists(folders.log):
        os.makedirs(folders.log)
    if not os.path.exists(log_file):
        os.mknod(log_file)
        return log_file

def get_last_log_file():
    if not os.path.exists(folders.log):
        os.makedirs(folders.log)
    return log_file

def write_log(log):
    log_file = get_last_log_file()
    now = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
    log_with_time = f"{now} {log}"
    with open(log_file, "a") as f:
        f.write(log_with_time + "\n")

def printError(error):
    text = f"{color.red} [ERROR] {color.reset}{error}{color.reset}"
    log_text = f"[ERROR] {error}"
    print(text)
    write_log(log_text)
def printInfo(info):
    text = f"{color.green} [INFO]  {color.reset}{info}{color.reset}"
    log_text = f"[INFO] {info}"
    print(text)
    write_log(log_text)
def printLog(log):
    text = f"{color.reset} [LOG]   {color.reset}{log}{color.reset}"
    log_text = f"[LOG]  {log}"
    print(text)
    write_log(log_text)
def printWarn(warn):
    text = f"{color.orange} [WARN]  {color.reset}{warn}{color.reset}"
    log_text = f"[WARN] {warn}"
    print(text)
    write_log(log_text)