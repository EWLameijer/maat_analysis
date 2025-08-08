import subprocess
from script_paths import MAAT_SCRIPTS_DIR 

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

filename = input("Please give the name of the file to analyze: ")
analyze_command = rf"python {MAAT_SCRIPTS_DIR}/miner/complexity_analysis.py {filename}"
output = subprocess.check_output(analyze_command, shell=True)
print(output)