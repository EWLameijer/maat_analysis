import os
import subprocess
from script_paths import MAAT_DIR

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ")
after = input("Please give the date after which the code should be analyzed: ")

create_log = f"git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after={after} > git_log_{name}.txt"
subprocess.check_output(create_log, shell=True)
print("Created git log")

run_maat = f"java -jar {MAAT_DIR}\\code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a coupling > coupling_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")
