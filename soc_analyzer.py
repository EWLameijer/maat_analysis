import os
import subprocess

from script_paths import MAAT_DIR

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ")

create_log = "git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after=2020-01-01 > git_log_" + name + ".txt"
subprocess.check_output(create_log, shell=True)
print("Created git log")

run_maat = fr"java -jar {MAAT_DIR}\code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a soc > soc_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")
