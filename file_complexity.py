import subprocess
from script_paths import MAAT_SCRIPTS_DIR 

filename = input("Please give the name of the file to analyze: ")
analyze_command = rf"python {MAAT_SCRIPTS_DIR}\miner\complexity_analysis.py {filename}"
output = subprocess.check_output(analyze_command, shell=True)
print(output)