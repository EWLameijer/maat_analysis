import os
import subprocess
from script_paths import MAAT_DIR

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ");
sinceDate = input("Please give the date since when the log should be analyzed (default 2021-08-01): ")
if (sinceDate == ""): sinceDate = "2020-08-01"

create_log = f"git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after={sinceDate} > git_log_" + name + ".txt"
subprocess.check_output(create_log, shell=True)
print("Created git log")

run_maat = rf"java -jar {MAAT_DIR}\code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a main-dev > main-dev_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")
