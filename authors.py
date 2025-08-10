import os
import subprocess

from common_code import git_utils
from script_paths import RUN_MAAT

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ")
git_utils.create_log(name)

run_maat = rf"{RUN_MAAT} -l git_log_{name}.txt -c git2 -a authors > authors_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")
