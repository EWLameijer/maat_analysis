import os
import subprocess
from script_paths import MAAT_DIR

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
sinceDate = input("Please give the date the git log has to be analyzed from (default 2020-01-01): ")
name = input("Please give an abbreviation for the file(s): ");

print("Creating git log")
create_log = f"git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after={sinceDate} > git_log_" + name + ".txt"
print("Executing: ", create_log)
subprocess.check_output(create_log, shell=True)
print("Created git log")

print("Running Codemaat")
run_maat = rf"java -jar {MAAT_DIR}\code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a coupling > coupling_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print(f"Ran Codemaat. Please check 'coupling_{name}.csv'.")
