from datetime import datetime
import os
import subprocess
import re

from common_code import one_year_ago

def to_analysis_path(filename: str) -> str: 
    return rf'{CODEMAAT_ANALYSIS_DIR}/{filename}'

CODEMAAT_ANALYSIS_DIR = 'codemaat-analysis'
DAYS_BETWEEN_REFRESHES = 21 # do about 1 analysis per sprint
GIT_LOG_FILE = 'git_log.txt'
GIT_LOG_PATH = to_analysis_path(GIT_LOG_FILE)
GIT_COUPLING_FILE = 'coupling.csv'
GIT_COUPLING_PATH = to_analysis_path(GIT_COUPLING_FILE)


class Analyzer:
    def __init__(self, git_repo, run_maat) -> None:
        self.git_repo = git_repo
        self.run_maat = run_maat
        self.__ensure_basic_analysis_exists()

    def __ensure_basic_analysis_exists(self): 
        print("Starting basic analysis")
        current_dir = os.getcwd()
        os.chdir(self.git_repo)
        if (CODEMAAT_ANALYSIS_DIR not in os.listdir()):
            self.__create_analysis_directory()
        self.__to_analysis_dir()
        if (not os.listdir() or self.__analysis_outdated()):
            self.__update_analysis_directory()
        else:
            print('Basic analysis has taken place!')
        os.chdir(current_dir)
        print("Ending basic analysis")

    def __create_analysis_directory(self):
        os.mkdir(CODEMAAT_ANALYSIS_DIR)

    def __to_analysis_dir(self):
        os.chdir(CODEMAAT_ANALYSIS_DIR)

    def __analysis_outdated(self):
        if not os.path.isfile(GIT_LOG_FILE): 
            return True
        created = os.path.getmtime(GIT_LOG_FILE) 
        now = datetime.now().timestamp()
        return now - created > DAYS_BETWEEN_REFRESHES * 24 * 3600
    
    def __update_analysis_directory(self):
        self.__create_git_log()
        self.__analyze_coupling()
    # get_authors_per_file()
    # count_lines()
    # get_activity_per_file()  

    def __create_git_log(self):
        DEFAULT_DATE = one_year_ago.one_year_ago_str()
        sinceDate = input(f"Please give the date since when the log should be analyzed (default {DEFAULT_DATE}): ")
        if (sinceDate == ""): sinceDate = DEFAULT_DATE
        print(f"Creating git log in '{os.getcwd()}'" )
        os.chdir(self.git_repo)
        create_log = fr"git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after={sinceDate} > {GIT_LOG_PATH}"
        subprocess.check_output(create_log, shell=True)
        print("Created git log")    

    def __analyze_coupling(self):
        MIN_OCCURRENCES_TOGETHER = 1 # CodeMaat's default is 5
        MIN_DEGREE = 1 # CodeMaat's default is 30

        print("Running Codemaat to analyze coupling")
        calculate_coupling_command = (rf"{self.run_maat} -l {GIT_LOG_PATH} -c git2 "
                                      rf"-a coupling -n {MIN_OCCURRENCES_TOGETHER} -i {MIN_DEGREE} > {GIT_COUPLING_PATH}")
        subprocess.check_output(calculate_coupling_command, shell=True)
        print(f"Analyzed coupling. Please check '{GIT_COUPLING_FILE}'.")


    def show_authors(self, filename: str):
        run_blame = f"git blame {filename}"
        output_as_bstring = subprocess.check_output(run_blame, shell=True)
        output = str(output_as_bstring, encoding='utf-8')
        current_author = 'unknown'
        linecounts = {}
        for line in output.splitlines():
            match = re.search(r"\((.*?)\s+\d{4}-\d{2}-\d{2}", line)
            if match:
                current_author = match.group(1).strip()
                if current_author not in linecounts: linecounts[current_author] = 0
                linecounts[current_author] += 1
        total_lines = sum(linecounts.values())
        print('\nAuthors:')
        for author, line_count in linecounts.items():
            print("{:20} {:5} {:10.1%}".format(author, line_count, line_count / total_lines))

