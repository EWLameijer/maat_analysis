import os
import subprocess
from script_paths import MAAT_DIR

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
DEFAULT_DATE = "2020-01-01"
sinceDate = input(f"Please give the date the git log has to be analyzed from (default {DEFAULT_DATE}): ")
if sinceDate == "": since_date = DEFAULT_DATE
module_overview = input("Please give the name of the module overview file: ")
name = input("Please give an abbreviation for the file(s): ")

print("Creating git log")
create_log = f"git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after={since_date} > git_log_" + name + ".txt"
print("Executing: ", create_log)
subprocess.check_output(create_log, shell=True)
print("Created git log")

print("Running Codemaat")
run_maat = rf"java -jar {MAAT_DIR}\code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a coupling -g {module_overview} --min-coupling 20 > module_coupling_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print(f"Ran Codemaat. Please check 'coupling_{name}.csv'.")