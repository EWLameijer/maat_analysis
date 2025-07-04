import os
import subprocess

punctuations = ".`'\",:;!?@#$%^&*({)[]{}/\\"
punctuation_dictionary = { ord(ch): None for ch in punctuations}

def remove_punctuation(input):
    return input.translate(punctuation_dictionary)

dir = input("Please give the directory to analyze: ")
os.chdir(dir)
message_file = input("Please give the name for the .txt file to create: ") + ".txt"
temp_file = "TEMP" + message_file 

create_log = f"git log --pretty=format:%s --after=2020-01-01 > {temp_file}"
subprocess.check_output(create_log, shell=True)

lowercased_text = ""
with open(temp_file) as f:
    for line in f:
        lowercased_text += remove_punctuation(line.lower())

output_file = open(message_file, "w")
output_file.write(lowercased_text)
os.remove(temp_file)
print(f"Please upload '{message_file}' to https://wordart.com/ .")

