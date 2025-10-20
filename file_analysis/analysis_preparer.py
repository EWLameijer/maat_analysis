import os
from datetime import datetime
import glob
import subprocess

from common_code import file_analysis, one_year_ago, string_utils
from file_analysis.code_units import CodeUnit, UnversionedCodeUnit, VersionedCodeUnit
from file_analysis.constants import (
    CODEMAAT_ANALYSIS_DIR,
    GIT_COUPLING_PATH,
    GIT_LOG_FILE,
    GIT_LOG_PATH,
    SYNONYMS_PATH,
)
from script_paths import RUN_MAAT

DAYS_BETWEEN_REFRESHES = 21  # do about 1 analysis per sprint
FORBIDDEN_PATHS = ["node_modules"]


def _contains_forbidden_path(filename: str) -> bool:
    if CODEMAAT_ANALYSIS_DIR in filename:
        return True
    for path in FORBIDDEN_PATHS:
        if path in filename:
            return True
    return False


class AnalysisPreparer:
    git_repo: str

    def __init__(self, git_repo: str):
        self.git_repo = git_repo
        self._ensure_basic_analysis_exists()

    def _ensure_basic_analysis_exists(self):
        current_dir = os.getcwd()
        os.chdir(self.git_repo)
        if CODEMAAT_ANALYSIS_DIR not in os.listdir():
            os.mkdir(CODEMAAT_ANALYSIS_DIR)
        os.chdir(CODEMAAT_ANALYSIS_DIR)
        if not os.listdir() or self._analysis_outdated():
            print("Performing basic analysis...")
            self._update_analysis_directory()
            print("Basic analysis completed.")
        else:
            print("Basic analysis has already taken place recently.")
        os.chdir(current_dir)

    def _analysis_outdated(self):
        if not os.path.isfile(GIT_LOG_FILE):
            return True
        created = os.path.getmtime(GIT_LOG_FILE)
        now = datetime.now().timestamp()
        return now - created > DAYS_BETWEEN_REFRESHES * 24 * 3600

    def _update_analysis_directory(self):
        self._create_git_log()
        self._analyze_file_synonyms()
        self._analyze_coupling()

    def _create_git_log(self):
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

    def _analyze_file_synonyms(self):
        print(f"Analyzing file history from '{self.git_repo}'.")
        file_synonyms = {}
        for raw_filename in glob.iglob(self.git_repo + "**/**", recursive=True):
            filename = string_utils.normalize_filename(raw_filename)
            if not _contains_forbidden_path(filename):
                synonyms = file_analysis.get_synonyms(filename, self.git_repo)
                if len(synonyms) > 0:
                    file_synonyms[filename] = synonyms

        filenames = sorted(file_synonyms.keys())
        lines = []
        for filename in filenames:
            synonyms = sorted(file_synonyms[filename])
            lines.append(f"{filename}: {', '.join(synonyms)}\n")
        with open(SYNONYMS_PATH, "w") as synonym_file:
            synonym_file.writelines(lines)

    def _analyze_coupling(self):
        MIN_OCCURRENCES_TOGETHER = 1  # CodeMaat's default is 5
        MIN_DEGREE = 1  # CodeMaat's default is 30

        print("Running Codemaat to analyze coupling")
        calculate_coupling_command = (
            rf"{RUN_MAAT} -l {GIT_LOG_PATH} -c git2 "
            rf"-a coupling -n {MIN_OCCURRENCES_TOGETHER} -i {MIN_DEGREE} > {GIT_COUPLING_PATH}"
        )
        subprocess.check_output(calculate_coupling_command, shell=True)
        print(f"Analyzed coupling. Please check '{self.git_repo}/{GIT_COUPLING_PATH}'.")
