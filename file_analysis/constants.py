CODEMAAT_ANALYSIS_DIR = "codemaat-analysis"
GIT_COUPLING_FILE = "coupling.csv"
GIT_LOG_FILE = "git-log.txt"
SYNONYMS_FILE = "file-synonyms.txt"


def to_analysis_path(filename: str) -> str:
    return rf"{CODEMAAT_ANALYSIS_DIR}/{filename}"


GIT_COUPLING_PATH = to_analysis_path(GIT_COUPLING_FILE)
GIT_LOG_PATH = to_analysis_path(GIT_LOG_FILE)
SYNONYMS_PATH = to_analysis_path(SYNONYMS_FILE)
