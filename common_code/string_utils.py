def get_normalized_filename() -> str:  
    raw_filename = input("Please give the name of the file: ")
    return raw_filename.replace('\\', '/')