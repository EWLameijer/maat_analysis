# copy this file into a scripts_paths.py and set the directories to those of your own system

PYTHON = 'python' # 'py' on some systems
TOOLS_DIR = r'C:/Development/tools'
MAAT_DIR = TOOLS_DIR
RUN_MAAT = f"java -jar {MAAT_DIR}/code-maat-1.0.4-standalone.jar"
CLOC = rf'{TOOLS_DIR}/cloc-@.@@.exe'
MAAT_SCRIPTS_DIR = fr"{MAAT_DIR}/maat-scripts"
TRANSFORM_DIR = fr"{MAAT_SCRIPTS_DIR}/transform"
MERGE_DIR = fr"{MAAT_SCRIPTS_DIR }/merge"