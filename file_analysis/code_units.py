# A CodeUnit could be loosely translated as a file, be it that the intuitive notion of a file
# with a constant name and changing content, so being an entity with the name as the identifier,
# may make sense for Word documents (like 'journal.doc'), but in code often the name is changed
# while the general purpose of the file contents remains the same; since the identity cannot be the
# name anymore, the code unit needs a separate identity, and can refer to a list of names
# Note that formally each name is only valid for a certain range of commits, but it may in most cases be
# an acceptable approximation that code units don't exchange names, which would mess up many maat analyses
# anyway...
# As I'm not using a database here, I don't need a separate primary key, object identity/uniqueness
# should be enough
class CodeUnit:
    git_root: str

    @staticmethod
    def _remove_root(root, full_name):
        return full_name.removeprefix(root + "/")


class UnversionedCodeUnit(CodeUnit):
    name: str

    def __init__(self, git_root, name):
        self.git_root = git_root
        self.name = self._remove_root(git_root, name)

    def __str__(self):
        return f"Unversioned file called '{self.git_root}/{self.name}'."


class VersionedCodeUnit(CodeUnit):
    names: list[str]
    _current_name_index: int | None

    current_name = property(
        lambda self: (
            None
            if self._current_name_index == None
            else self.names[self._current_name_index]
        )
    )

    def __init__(self, full_name, git_root, synonyms: set[str]):
        self.git_root = git_root
        synonyms_list = list(synonyms)
        current_name = self._remove_root(git_root, full_name)
        self.names = (
            synonyms_list
            if current_name in synonyms_list
            else synonyms_list + [current_name]
        )
        self._current_name_index = self.names.index(current_name)

    def __str__(self):
        other_names = set(self.names) - set(self.current_name)
        return f"Versioned file called '{self.git_root}/{self.current_name}', previous names were {other_names}."

