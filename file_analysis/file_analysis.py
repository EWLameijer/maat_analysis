import os
import subprocess


def get_synonyms(filename: str, git_repo: str) -> set[str]:
    os.chdir(git_repo)
    run_blame = f"git blame {filename}"
    output_as_bstring = subprocess.check_output(run_blame, shell=True)
    output = str(output_as_bstring, encoding="utf-8")
    synonyms = {filename.removeprefix(git_repo + "/")}
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
