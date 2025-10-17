import os
from pathlib import Path
import subprocess


def get_synonyms(full_filename: str, git_repo: str) -> set[str]:
    os.chdir(git_repo)
    if not Path(full_filename).is_file():
        print(f"Can't find '{full_filename}'!")
        return set()
    is_file_managed_command = f'git ls-files "{full_filename}"'
    is_managed = subprocess.check_output(is_file_managed_command, shell=True)
    if not is_managed:
        return set()
    run_blame = f'git blame "{full_filename}"'
    # print(f"Running command '{run_blame}'.")
    output_as_bstring = subprocess.check_output(run_blame, shell=True)
    output = str(output_as_bstring, encoding="utf-8")
    shorter_name = full_filename.removeprefix(git_repo + "/")
    # print(
    #     f"Removing prefix '{git_repo}' from '{full_filename}', making '{shorter_name}'."
    # )
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

    return synonyms
