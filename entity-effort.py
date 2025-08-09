import os
import subprocess

from common_code import git_utils
from script_paths import MAAT_DIR

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ")
spec_file = input("If you have a spec file (directory => your-name-for-package), enter it here: ")
spec_path = f"-g {spec_file}" if spec_file != "" else ""

git_utils.create_log(name)

run_maat = rf"java -jar {MAAT_DIR}/code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a entity-effort {spec_path} > entity-effort_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")
