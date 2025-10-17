import subprocess
import os

from .one_year_ago import one_year_ago_str


def create_log(name: str):
    __create_log_with_format(
        name, "--all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames"
    )


def create_abbreviated_log(name: str):
    __create_log_with_format(name, "--pretty=format:%s")


def find_git_root(filename: str) -> str | None:
    normalized_filename = filename.replace("\\", "/")
    path_elements = normalized_filename.split("/")
    for remove_steps in range(1, len(path_elements)):
        # +"/" because on Windows C: will refer to original directory, NOT the actual C-drive, which is "C:\"
        path = "/".join(path_elements[:-remove_steps]) + "/"
        if os.path.exists(path):
            files = os.listdir(path)
            is_root = ".git" in files
            if is_root:
                return path.strip("/")  # remove superfluous "/"
    return None


def __create_log_with_format(name: str, format: str):
    DEFAULT_DATE = one_year_ago_str()
    fromDate = input(
        f"Please give the date since when the log should be analyzed (default {DEFAULT_DATE}): "
    )
    if fromDate == "":
        fromDate = DEFAULT_DATE
    print("Creating git log")
    create_log = f"git log {format} --after={fromDate} > git_log_{name}.txt"
    subprocess.check_output(create_log, shell=True)
    print("Created git log")
