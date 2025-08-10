import os
import shutil
import subprocess

from common_code import git_utils
from script_paths import CLOC, MAAT_DIR, MERGE_DIR, PYTHON, TRANSFORM_DIR 

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS
# ALERT: YOU MAY WANT TO REMOVE NODE_MODULES FOR CLOC

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
output_name = input("Please give an abbreviation for the output file(s): ")
git_utils.create_log(output_name)

print("Running Codemaat to gather git activity per file")
run_maat = rf"java -jar {MAAT_DIR}/code-maat-1.0.4-standalone.jar -l git_log_{output_name}.txt -c git2 -a revisions > activity_{output_name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")

directories_to_exclude = ["build", "coverage", "dist", ".idea", "node_modules", "venv" ]
directories_to_exclude_list = '|'.join(directories_to_exclude)
directories_to_exclude_text = f"({', '.join(directories_to_exclude)})"

print(f"Using cloc to count lines, excluding {directories_to_exclude_text}")
run_cloc =rf'{CLOC} ./ --unix --by-file --csv --exclude-ext=adoc,csv,json,md,txt --fullpath --not-match-d="({directories_to_exclude_list})" --report-file=complexity_{output_name}.csv'
subprocess.check_output(run_cloc, shell=True)
print("Gathered line counts")

print("Looking for hotspots - by combining file size data with file frequency change data")
create_hotspots = rf"{PYTHON} {MERGE_DIR}/merge_comp_freqs.py activity_{output_name}.csv complexity_{output_name}.csv > hotspots_{output_name}.csv"
subprocess.check_output(create_hotspots, shell=True)
print("Found hotspots")

print("Creating a JSON graph")
create_json_graph = rf"{PYTHON} {TRANSFORM_DIR}/csv_as_enclosure_json.py --structure complexity_{output_name}.csv --weights activity_{output_name}.csv > hotspots_{output_name}.json"
subprocess.check_output(create_json_graph, shell=True)
print("Created JSON graph")

print("Display graph on server")
display_graph_on_server = shutil.copy(rf"hotspots_{output_name}.json", f"{TRANSFORM_DIR}/hotspots.json")
print(f"Check http://localhost:8000/crime-scene-hotspots.html (remember to start a local server first at maat-scripts/transform, for example with '{PYTHON} -m http.server')")

