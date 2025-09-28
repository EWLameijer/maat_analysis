import csv
from datetime import datetime
import os
import re
import subprocess

from common_code import git_utils, one_year_ago


def to_analysis_path(filename: str) -> str:
    return rf"{CODEMAAT_ANALYSIS_DIR}/{filename}"


CODEMAAT_ANALYSIS_DIR = "codemaat-analysis"
DAYS_BETWEEN_REFRESHES = 21  # do about 1 analysis per sprint
GIT_LOG_FILE = "git_log.txt"
GIT_LOG_PATH = to_analysis_path(GIT_LOG_FILE)
GIT_COUPLING_FILE = "coupling.csv"
GIT_COUPLING_PATH = to_analysis_path(GIT_COUPLING_FILE)


class Analyzer:
    def __init__(self, git_repo, run_maat) -> None:
        self.git_repo = git_repo
        self.run_maat = run_maat
        self.__ensure_basic_analysis_exists()

    def __ensure_basic_analysis_exists(self):
        current_dir = os.getcwd()
        os.chdir(self.git_repo)
        if CODEMAAT_ANALYSIS_DIR not in os.listdir():
            self.__create_analysis_directory()
        self.__to_analysis_dir()
        if not os.listdir() or self.__analysis_outdated():
            print("Performing basic analysis...")
            self.__update_analysis_directory()
            print("Basic analysis completed.")
        else:
            print("Basic analysis has already taken place recently.")
        os.chdir(current_dir)

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
        sinceDate = input(
            f"Please give the date since when the log should be analyzed (default {DEFAULT_DATE}): "
        )
        if sinceDate == "":
            sinceDate = DEFAULT_DATE
        print(f"Creating git log in '{os.getcwd()}'")
        os.chdir(self.git_repo)
        create_log = rf"git log --all --numstat --date=short --pretty=format:--%h--%ad--%aN --no-renames --after={sinceDate} > {GIT_LOG_PATH}"
        subprocess.check_output(create_log, shell=True)
        print("Created git log")

    def __analyze_coupling(self):
        MIN_OCCURRENCES_TOGETHER = 1  # CodeMaat's default is 5
        MIN_DEGREE = 1  # CodeMaat's default is 30

        print("Running Codemaat to analyze coupling")
        calculate_coupling_command = (
            rf"{self.run_maat} -l {GIT_LOG_PATH} -c git2 "
            rf"-a coupling -n {MIN_OCCURRENCES_TOGETHER} -i {MIN_DEGREE} > {GIT_COUPLING_PATH}"
        )
        subprocess.check_output(calculate_coupling_command, shell=True)
        print(f"Analyzed coupling. Please check '{GIT_COUPLING_FILE}'.")

        # Now: for each file in the two lines, get all synonyms
        # So first read in all files, get the data structure in memory

        # def get_commit_count(filename: str) -> int:

    # number_of_commits = -1
    # for line in csv.reader(open(ACTIVITY_PATH)):
    #     current_file = line[0]
    #     if current_file and filename.endswith(current_file.strip('.')):
    #         number_of_commits = int(line[1])
    # if (number_of_commits < 0):
    #     print(f"'{filename}' not found!")
    #     return number_of_commits
    # higher_counts = 0
    # total_files = 0
    # for line in csv.reader(open(ACTIVITY_PATH)):
    #     if line[0] and line[0] != 'entity':
    #         total_files += 1
    #         if int(line[1]) >= number_of_commits: higher_counts += 1
    # top_percentage = 100.0 * higher_counts / total_files
    # print(f"'{filename}' has {number_of_commits} commits, is in the top {top_percentage:6.2f}%")
    # return number_of_commits

    def show_authors(self, filename: str):
        run_blame = f"git blame {filename}"
        output_as_bstring = subprocess.check_output(run_blame, shell=True)
        output = str(output_as_bstring, encoding="utf-8")
        current_author = "unknown"
        linecounts = {}
        for line in output.splitlines():
            match = re.search(r"\((.*?)\s+\d{4}-\d{2}-\d{2}", line)
            if match:
                current_author = match.group(1).strip()
                if current_author not in linecounts:
                    linecounts[current_author] = 0
                linecounts[current_author] += 1
        total_lines = sum(linecounts.values())
        print("\nAuthors:")
        for author, line_count in linecounts.items():
            print(
                "{:20} {:5} {:10.1%}".format(
                    author, line_count, line_count / total_lines
                )
            )
        print()

    def show_coupling(self, full_filename: str):
        git_root = git_utils.find_git_root(full_filename)
        if git_root is None:
            print(f"'{full_filename}' is not in a git repository")
            return
        filename = full_filename.removeprefix(git_root + "/")
        raw_couplings = [
            line_elements for line_elements in csv.reader(open(GIT_COUPLING_PATH))
        ]
        couplings = {}
        for [
            first_filename,
            second_filename,
            degree_as_text,
            count_as_text,
        ] in raw_couplings:
            if first_filename != filename and second_filename != filename:
                continue
            partner = second_filename if filename == first_filename else first_filename
            couplings[partner] = (int(degree_as_text), int(count_as_text))

        if len(couplings) == 0:
            print("No significant file couplings found!")
        else:
            print("Couplings found with:")
            for other_file, (percentage, counts) in sorted(
                couplings.items(), reverse=True, key=lambda e: e[1][1]
            ):
                print(
                    f"\t- '{other_file}': {percentage}% coupled, {counts} common commits."
                )
        print()
