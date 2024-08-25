import os
from data.var import *
from datetime import datetime


timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
log_file = os.path.join(log_folder_path, f"{timestamp}.log")

def get_next_log_file():
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    if not os.path.exists(log_file):
        os.mknod(log_file)
        return log_file

def get_last_log_file():
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    return log_file

def write_log(log):
    log_file = get_last_log_file()
    now = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
    log_with_time = f"{now} {log}"
    with open(log_file, "a") as f:
        f.write(log_with_time + "\n")

def printError(error):
    text = f"{red} [ERROR] {reset}{error}{reset}"
    log_text = f"[ERROR] {error}"
    print(text)
    write_log(log_text)
def printInfo(info):
    text = f"{green} [INFO]  {reset}{info}{reset}"
    log_text = f"[INFO] {info}"
    print(text)
    write_log(log_text)
def printLog(log):
    text = f"{reset} [LOG]   {reset}{log}{reset}"
    log_text = f"[LOG]  {log}"
    print(text)
    write_log(log_text)
def printWarn(warn):
    text = f"{orange} [WARN]  {reset}{warn}{reset}"
    log_text = f"[WARN] {warn}"
    print(text)
    write_log(log_text)