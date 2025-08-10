import subprocess

from .one_year_ago import one_year_ago_str  

def create_log(name: str):
    __create_log_with_format(name, "--all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames")

def create_abbreviated_log(name: str):
    __create_log_with_format(name, "--pretty=format:%s")

def __create_log_with_format(name: str, format: str):
    DEFAULT_DATE = one_year_ago_str()
    fromDate = input(f"Please give the date since when the log should be analyzed (default {DEFAULT_DATE}): ")
    if (fromDate == ""): fromDate = DEFAULT_DATE
    print("Creating git log")
    create_log = f"git log {format} --after={fromDate} > git_log_{name}.txt"
    subprocess.check_output(create_log, shell=True)
    print("Created git log")
