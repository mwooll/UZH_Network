import os


def parse_and_create_directories(folder=""):
    source_dir = "data/source/" + folder
    text_dir = "data/text/"
    csv_dir = "data/csv/"
    write_dirs = [text_dir, csv_dir]

    # directory
    dirs = next(os.walk(source_dir))[1]
    create_subdirectories(write_dirs, dirs)

def create_subdirectories(folders, sub_dirs):
    for folder in folders:
        for sub in sub_dirs:
            path = folder + sub
            
            if not os.path.isdir(path):
                os.mkdir(path)

if __name__ == "__main__":
    parse_and_create_directories()