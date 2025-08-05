import os
import subprocess
from script_paths import CLOC, MAAT_DIR, MERGE_DIR, PYTHON, TRANSFORM_DIR 

dir = input("Please give the directory in which the git repository of the file is housed: ")
os.chdir(dir)
output_name = input("Please give the path for the file you want to find the last commit of: ")
show_last_commit_date = f'git log -1 --format="%ad" --date=short {output_name}'
date_as_bstring = subprocess.check_output(show_last_commit_date, shell=True)
date_as_string = str(date_as_bstring, encoding='utf-8')
print(date_as_string)
