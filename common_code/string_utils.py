def get_normalized_filename() -> str:  
    raw_filename = input("Please give the name of the file: ")
    return raw_filename.replace('\\', '/')

def simplify_prefixes(filenames: list[str]) -> list[str]: 
    split_strings = [filename.split("/") for filename in filenames]
    while True:
        prefix = None 
        for string in split_strings:
            current_prefix = string[0]
            if prefix != current_prefix:
                if prefix == None: 
                    prefix = current_prefix
                else:
                    shortened_paths = ["/".join(split_string) for split_string in split_strings]
                    return shortened_paths 
        # all prefixes are the same
        split_strings = [split_string[1:] for split_string in split_strings]

