import csv

import os
import re
import subprocess

from common_code import file_analysis, git_utils
from file_analysis.analysis_preparer import AnalysisPreparer
from file_analysis.constants import GIT_COUPLING_PATH, SYNONYMS_PATH
from pathlib import Path


class Analyzer:
    def __init__(self, git_repo: str, filename: str):
        self.git_repo = git_repo
        self.filename = filename

        # ensure files exist to base analysis on
        AnalysisPreparer(git_repo)

    def get_synonyms(self) -> set[str]:
        caller_dir = os.getcwd()
        os.chdir(self.git_repo)
        run_blame = f'git blame "{self.filename}"'
        output_as_bstring = subprocess.check_output(run_blame, shell=True)
        output = str(output_as_bstring, encoding="utf-8")
        shorter_name = self.filename.removeprefix(self.git_repo + "/")
        synonyms = {shorter_name}
        for line in output.split("\n"):
            elements = line.split()
            if len(elements) > 1:
                filename = line.split()[1]

                # git blame has different output for files that have and that have
                # no renamings - if there aren't any renamings, the second element
                # in the line is the author name, not the name of the original file
                if not filename.startswith("("):
                    synonyms.add(filename)
        os.chdir(caller_dir)
        return synonyms

    def show_authors(self):
        caller_dir = os.getcwd()
        os.chdir(self.git_repo)
        run_blame = f"git blame {self.filename}"
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
        os.chdir(caller_dir)
        total_lines = sum(linecounts.values())
        title = "Author" if len(linecounts) == 1 else "Authors"
        print(f"\n{title}:")
        for author, line_count in linecounts.items():
            print(
                "{:20} {:5} {:10.1%}".format(
                    author, line_count, line_count / total_lines
                )
            )
        print()

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

    def get_current_name(self, full_filename: str) -> list[str]:
        target_filename = self._get_name_in_repo(full_filename)
        all_current_names = []
        with open(SYNONYMS_PATH) as synonyms_file:
            for line in synonyms_file:
                if target_filename in line:
                    current = line.split(": ")[0]
                    all_current_names.append(current)
        return all_current_names

    def _get_name_in_repo(self, full_filename):
        return full_filename.removeprefix(self.git_repo + "/")

    #
    #

    def show_coupling(self, full_filename: str):
        git_root = git_utils.find_git_root(full_filename)
        if git_root is None:
            print(f"'{full_filename}' is not in a git repository")
            return
        synonyms = file_analysis.get_synonyms(full_filename, self.git_repo)
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
            for synonym in synonyms:
                if first_filename != synonym and second_filename != synonym:
                    continue
                partner = (
                    second_filename if synonym == first_filename else first_filename
                )
                couplings[partner] = (int(degree_as_text), int(count_as_text))

        if len(couplings) == 0:
            print("No significant file couplings found!")
        else:
            print("Couplings found with:")
            for other_file, (percentage, counts) in sorted(
                couplings.items(), reverse=True, key=lambda e: e[1][1]
            ):
                current_names = [
                    self._get_name_in_repo(filename)
                    for filename in self.get_current_name(other_file)
                ]
                if len(current_names) == 0:
                    continue  # file is not in version control
                display_name = (
                    current_names if len(current_names) > 1 else current_names[0]
                )
                print(
                    f"\t- '{display_name}': {percentage}% coupled, {counts} common commits."
                )
        print()


def get_analyzer_or_throw(filename: str) -> Analyzer:
    git_repo = git_utils.find_git_root(filename)
    if git_repo == None:
        raise Exception(f"Repository for '{filename}' not found.")
    if not _under_version_control(filename, git_repo):
        raise Exception(f"The file '{filename}' is not under Git control.")
    return Analyzer(git_repo, filename)


def _under_version_control(filename: str, git_repo: str) -> bool:
    caller_dir = os.getcwd()
    os.chdir(git_repo)
    if not Path(filename).is_file():
        os.chdir(caller_dir)
        return False
    is_file_managed_command = f'git ls-files "{filename}"'
    is_managed = subprocess.check_output(is_file_managed_command, shell=True)
    os.chdir(caller_dir)
    return bool(is_managed)
