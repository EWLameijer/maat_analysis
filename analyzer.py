import os
import subprocess

SCRIPT_DIR = "C:\\Users\\LalaShops\\Desktop\\JLoc\\" 
MAAT_DIR = "D:\\Development\\Tornhill\\maat-scripts\\transform\\"

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ");

create_log = "git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after=2021-08-01 > git_log_" + name + ".txt"
subprocess.check_output(create_log, shell=True)
print("Created git log")

run_maat = f"java -jar {SCRIPT_DIR}code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a revisions > activity_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")

run_cloc =f"{SCRIPT_DIR}cloc-2.02.exe ./ --unix --by-file --csv --quiet --report-file=complexity_{name}.csv"
subprocess.check_output(run_cloc, shell=True)
print("Gathered line counts")

create_hotspots = f"python {SCRIPT_DIR}merge_comp_freqs.py activity_{name}.csv complexity_{name}.csv > hotspots_{name}.csv"
subprocess.check_output(create_hotspots, shell=True)
print("Found hotspots")

create_json_graph = f"python {MAAT_DIR}csv_as_enclosure_json.py --structure complexity_{name}.csv --weights activity_{name}.csv > hotspots_{name}.json"
subprocess.check_output(create_json_graph, shell=True)
print("Created JSON graph")

display = f"copy hotspots_{name}.json {MAAT_DIR}hotspots.json"
subprocess.check_output(display, shell=True)
print("Check localhost:8080")

