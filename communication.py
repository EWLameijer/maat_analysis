import os
import subprocess

from common_code import git_utils
from script_paths import MAAT_DIR

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ")
git_utils.create_log(name)

run_maat = rf"java -jar {MAAT_DIR}/code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a communication > communication_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")
