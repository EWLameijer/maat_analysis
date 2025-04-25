import os
import subprocess
from script_paths import CLOC_DIR, MAAT_DIR, MERGE_DIR, TRANSFORM_DIR 

# ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS
# ALERT: YOU MAY WANT TO REMOVE NODE_MODULES FOR CLOC


dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ");
sinceDate = input("Please give the date since when the log should be analyzed (default 2021-08-01): ")
if (sinceDate == "") sinceDate = "2021-08-01"

create_log = "git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after={sinceDate} > git_log_" + name + ".txt"
subprocess.check_output(create_log, shell=True)
print("Created git log")

run_maat = rf"java -jar {MAAT_DIR}\code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a revisions > activity_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")

# run_cloc =rf"{CLOC_DIR}\cloc-2.04.exe ./ --unix --by-file --csv --quiet --report-file=complexity_{name}.csv"
run_cloc =rf"{CLOC_DIR}\cloc-2.04.exe ./ --unix --by-file --csv --exclude-ext=csv,json,txt --report-file=complexity_{name}.csv"
subprocess.check_output(run_cloc, shell=True)
print("Gathered line counts")

create_hotspots = rf"python {MERGE_DIR}\merge_comp_freqs.py activity_{name}.csv complexity_{name}.csv > hotspots_{name}.csv"
subprocess.check_output(create_hotspots, shell=True)
print("Found hotspots")

create_json_graph = rf"python {TRANSFORM_DIR}\csv_as_enclosure_json.py --structure complexity_{name}.csv --weights activity_{name}.csv > hotspots_{name}.json"
subprocess.check_output(create_json_graph, shell=True)
print("Created JSON graph")

display = rf"copy hotspots_{name}.json {TRANSFORM_DIR}\hotspots.json"
subprocess.check_output(display, shell=True)
print("Check localhost:8080")

