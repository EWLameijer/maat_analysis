import os
import subprocess

from common_code import git_utils
from script_paths import MAAT_DIR

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

dir = input("Please give the directory to analyze: ")
os.chdir(dir)

module_overview = input("Please give the name of the module overview file: ")
name = input("Please give an abbreviation for the file(s): ")
git_utils.create_log(name)

print("Running Codemaat")
run_maat = rf"java -jar {MAAT_DIR}/code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a coupling -g {module_overview} --min-coupling 20 > module_coupling_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print(f"Ran Codemaat. Please check 'coupling_{name}.csv'.")