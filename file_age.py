import os
import subprocess
from common_code.git_utils import find_git_root
from script_paths import CLOC, MAAT_DIR, MERGE_DIR, PYTHON, TRANSFORM_DIR 

filename = input("Please give the path for the file you want to find the last commit of: ")
git_root = find_git_root(filename)
print(git_root)
if git_root is None:
    print(f"'{filename}' is not version-controlled!")
else: 
    os.chdir(git_root)
    show_last_commit_date = f'git log -1 --format="%ad" --date=short {filename}'
    date_as_bstring = subprocess.check_output(show_last_commit_date, shell=True)
    date_as_string = str(date_as_bstring, encoding='utf-8')
    print(date_as_string)
