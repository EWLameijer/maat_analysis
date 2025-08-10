import os
import subprocess

from common_code import git_utils
from script_paths import RUN_MAAT

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

dir = input("Please give the directory to analyze: ")
os.chdir(dir)

module_overview = input("Please give the name of the module overview file: ")
name = input("Please give an abbreviation for the file(s): ")
git_utils.create_log(name)

print("Running Codemaat")
run_maat = rf"{RUN_MAAT} -l git_log_{name}.txt -c git2 -a coupling -g {module_overview} --min-coupling 20 > module_coupling_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print(f"Ran Codemaat. Please check 'coupling_{name}.csv'.")