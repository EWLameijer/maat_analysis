import subprocess

filename = input("Please give the name of the file to analyze: ")
analyze_command = f"python D:\\Development\\Tornhill\\maat-scripts\\miner\\complexity_analysis.py {filename}"
output = subprocess.check_output(analyze_command, shell=True)
print(output)