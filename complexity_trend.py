import subprocess
import os
from script_paths import MAAT_SCRIPTS_DIR

dir = input("Please give the git root of the project: ")
filename = input("Please give the name of the file to analyze (LOCAL PATH FROM ROOT, WITH FORWARD SLASHES): ")
initial_commit = input("Please give the hash of the initial commit: ")
final_commit = input("Please give the hash of the final commit: ")
output = input("Please give the name for the output file: ")

os.chdir(dir)
analyze_command = f"python {MAAT_SCRIPTS_DIR}\\miner\\git_complexity_trend.py --start {initial_commit} --end {final_commit} --file {filename} > {output}.csv"
subprocess.check_output(analyze_command, shell=True)
