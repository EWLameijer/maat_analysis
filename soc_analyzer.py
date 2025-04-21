import os
import subprocess

SCRIPT_DIR = "C:\\Users\\LalaShops\\Desktop\\JLoc\\" 
MAAT_DIR = "D:\\Development\\Tornhill\\maat-scripts\\transform\\"

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
name = input("Please give an abbreviation for the file(s): ");

create_log = "git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after=2020-01-01 > git_log_" + name + ".txt"
subprocess.check_output(create_log, shell=True)
print("Created git log")

run_maat = f"java -jar {SCRIPT_DIR}code-maat-1.0.4-standalone.jar -l git_log_{name}.txt -c git2 -a soc > soc_{name}.csv"
subprocess.check_output(run_maat, shell=True)
print("Ran Codemaat")
