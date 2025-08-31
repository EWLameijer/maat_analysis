


# import csv
# from datetime import datetime 
# import os
# import subprocess

# from script_paths import CLOC, RUN_MAAT # , MERGE_DIR, PYTHON, TRANSFORM_DIR 
# from common_code import one_year_ago

# # ALERT: ENSURE PYTHON3-BRANCH IS CHECKED OUT FROM THE MAAT-SCRIPTS
# # ALERT: YOU MAY WANT TO REMOVE NODE_MODULES FOR CLOC

# CODEMAAT_ANALYSIS_DIR = 'codemaat-analysis'
# 
# GIT_LOG_PATH = rf'{CODEMAAT_ANALYSIS_DIR}\{GIT_LOG_FILE}'
# COMPLEXITY_FILE = 'complexity.csv'
# COMPLEXITY_PATH = rf'{CODEMAAT_ANALYSIS_DIR}\{COMPLEXITY_FILE}'
# ACTIVITY_FILE = 'activity.csv'
# ACTIVITY_PATH = rf'{CODEMAAT_ANALYSIS_DIR}\{ACTIVITY_FILE}'
# ENTITY_EFFORT_PATH = rf'{CODEMAAT_ANALYSIS_DIR}\entity-effort.csv'
# 



# def get_git_log():
#     DEFAULT_DATE = one_year_ago.one_year_ago_str()
#     sinceDate = input(f"Please give the date since when the log should be analyzed (default {DEFAULT_DATE}): ")
#     if (sinceDate == ""): sinceDate = DEFAULT_DATE
#     print("Creating git log")
#     create_log = fr"git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after={sinceDate} > {GIT_LOG_PATH}"
#     subprocess.check_output(create_log, shell=True)
#     print("Created git log")

# def get_authors_per_file():
#     print('Detect authors per file (use a .mailmap file in the root of your repo to get rid of aliases, lines like "Firstname Lastname <address@provider.com>")')
#     all_authors = rf"{RUN_MAAT} -l {GIT_LOG_PATH} -c git2 -a entity-effort > {ENTITY_EFFORT_PATH}"
#     subprocess.check_output(all_authors, shell=True)
#     print("Completed authors per file")

# def count_lines():
#     print("Using cloc to count lines")
#     run_cloc =rf"{CLOC} ./ --unix --by-file --csv --exclude-ext=adoc,csv,json,md,txt --fullpath --not-match-d=.*node_modules --report-file={COMPLEXITY_PATH}"
#     subprocess.check_output(run_cloc, shell=True)
#     print("Gathered line counts")

# def get_activity_per_file():
#     print("Running Codemaat to gather git activity per file")
#     run_maat = rf"{RUN_MAAT} -l  {GIT_LOG_PATH} -c git2 -a revisions > {ACTIVITY_PATH}"
#     subprocess.check_output(run_maat, shell=True)
#     print("Ran Codemaat")






# def to_main_dir():
#     os.chdir(dir)



# def sort_by_element(list):
#     return int(list[2])

# def get_authors(filename):
#     # IMPORTANT! Especially with file renaming, authoring is more reliable when done from git blame
#     file_data = []
#     for line in csv.reader(open(ENTITY_EFFORT_PATH)):
#         if filename.endswith(line[0]): file_data.append(line)
    
#     authors = sorted(set(row[1] for row in file_data))
#     contributions_per_author = {
#         author: sum(int(row[2]) for row in file_data if row[1] == author)
#         for author in authors
#     }
#     total_contributions = sum(contributions_per_author.values())

#     for author in authors:
#         contribution = contributions_per_author[author]
#         percentage = contribution * 100.0 / total_contributions
#         print(f"{author:>20}: {contribution:4d}   {percentage:6.2f}%")

# def get_line_count(filename: str) -> int:
#     number_of_lines = -1
#     for line in csv.reader(open(COMPLEXITY_PATH)):
#         current_file = line[1]
#         if current_file and filename.endswith(current_file.strip('.')): 
#             number_of_lines = int(line[4])
#     if (number_of_lines < 0): 
#         print(f"'{filename}' not found!")
#         return number_of_lines
#     higher_counts = 0
#     total_files = 0
#     for line in csv.reader(open(COMPLEXITY_PATH)):
#         if line[1] and line[1] != 'filename':
#             total_files += 1
#             if int(line[4]) >= number_of_lines: higher_counts += 1
#     top_percentage = 100.0 * higher_counts / total_files
#     print(f"'{filename}' has {number_of_lines} code lines, is in the top {top_percentage:6.2f}%")
#     return number_of_lines

# def get_commit_count(filename: str) -> int:
#     number_of_commits = -1
#     for line in csv.reader(open(ACTIVITY_PATH)):
#         current_file = line[0]
#         if current_file and filename.endswith(current_file.strip('.')): 
#             number_of_commits = int(line[1])
#     if (number_of_commits < 0): 
#         print(f"'{filename}' not found!")
#         return number_of_commits
#     higher_counts = 0
#     total_files = 0
#     for line in csv.reader(open(ACTIVITY_PATH)):
#         if line[0] and line[0] != 'entity':
#             total_files += 1
#             if int(line[1]) >= number_of_commits: higher_counts += 1
#     top_percentage = 100.0 * higher_counts / total_files
#     print(f"'{filename}' has {number_of_commits} commits, is in the top {top_percentage:6.2f}%")
#     return number_of_commits

# def get_file_stats(filename: str):
#     print("File stats:")
#     line_count = get_line_count(filename)
#     commit_count = get_commit_count(filename)
    
#     # get lines of code of the file
    
#     # get number of commits of the file
#     # print lines of code * number of commits (hotness)
#     # get top 

# def calculate_blame(filename: str):
#     run_blame = f"git blame --porcelain {filename}"
#     output_as_bstring = subprocess.check_output(run_blame, shell=True)
#     output = str(output_as_bstring, encoding='utf-8')
#     #print(output)
#     current_author = 'unknown'
#     linecounts = {}
#     for line in output.splitlines():
#         # print("line:", line)
#         if line.startswith("author "):
#             current_author = line.removeprefix("author ")
#             #print(current_author)
#             if current_author not in linecounts: linecounts[current_author] = 0
#         if line.startswith('\t'):
#             # print("Line found!!")
#             linecounts[current_author] += 1
#             print(line, current_author, linecounts[current_author])
#     for author, lines in linecounts.items():
#         print(author, lines)
#     # for C:\development\AttendanceTracker\frontend\src\lesson-management-page\LessonManagement.tsx
#     # golden standard: 396 lines, 212 EW 184 MtP
#     # from porcelain: 396 lines, 267 EW 129 MtP WHY?
#     # first lines go as expected, but const lessonmanagement would be from EW according to blame, Mark according to Porcelain?
#     # Ah! porcelain creates a catalogue of commits with author, and then just uses the commit hash
#     # Can I use normal blame after the first ")" (and author after first '(')?

# # IMPORTANT: find all old pseudonyms of files!



# # Start the programme

# dir = input('Please give the directory to analyze: ')
# to_main_dir()

# # Step 2: check if there is already a codemaat-analysis directory there, or if it is outdated. 


# if (CODEMAAT_ANALYSIS_DIR not in os.listdir()):
#     create_analysis_directory()

# to_analysis_dir()
# if (not os.listdir() or analysis_outdated()):
#     to_main_dir()
#     update_analysis_directory()

# else:
#     print('Basic analysis has taken place!')

# to_main_dir()

# # What do I want? First: who has worked on a certain file

# filename = input('What is the path of the file you wish to analyze? ')
# stripped_filename = filename.strip("\"'")
# filename_with_slashes = stripped_filename.replace('\\','/')
# get_file_stats(filename_with_slashes)
# get_authors(filename_with_slashes)
# calculate_blame(filename_with_slashes)

from common_code import git_utils, string_utils
from file_analysis import analyzer, file_analysis
from script_paths import RUN_MAAT

# Goals
# 1. To ask for help, find out authors of the file (USE GIT BLAME!, likely with --porcelain)
# 2. To find other files to potentially modify, find the coupling
# 3. To get danger status, get 
#   sum of coupling (also relative)
#   DONE! number of lines (also relative)
#   number of commits (also relative)
#   hotness (# lines * # commits, also relative)

# To do my analysis, I need both the name of the file and of the repository. Fortunately, the filename
# implies the repository name/

# from the user, I need:
# he name of the file (the name of the file implies git repo?)

# ask for the name of the file
filename = string_utils.get_normalized_filename()
git_repo = git_utils.find_git_root(filename)
if git_repo == None: 
    print("Repository for '{filename}' not found.")
    exit()

print(f"The file '{filename}' is in repository '{git_repo}'.")

analyzer = analyzer.Analyzer(git_repo, RUN_MAAT)

# get the names of the file
synonyms = file_analysis.get_synonyms(filename, git_repo)
nice_synonyms = string_utils.simplify_prefixes(list(synonyms))
print("\nThe synonyms of the file are:")
for nice_synonym in nice_synonyms: print(f'- {nice_synonym}')

analyzer.calculate_blame(filename)

# find the authors (try regular git blame)





