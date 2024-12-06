import os

def rename_files(source_dir):
    files_renamed = {}
    for path, dirs, files in os.walk(source_dir):
        for file in files:
            if "courses" in file:
                new_name = file.replace("courses", "time_schedules")
                os.renames(path + "/" + file, path + "/" + new_name)
                files_renamed[file] = new_name
    return files_renamed
                

def prepare_directories(source_dir):    
    # deleting hidden "[].pdf.Zone.Identifier" files
    files_removed = []
    for path, dirs, files in os.walk(source_dir):
        for file in files:
            if "Zone.Identifier" in file:
                os.remove(path + "/" + file)
                files_removed.append(file)

    # creating subdirectories for /text and /csv
    text_dir = "data/text/"
    csv_dir = "data/csv/"
    write_dirs = [text_dir, csv_dir]

    dirs = next(os.walk(source_dir))[1]
    new = create_subdirectories(write_dirs, dirs)

    return files_removed, new

def create_subdirectories(folders, sub_dirs):
    new_folders = []
    new_files = []
    for folder in folders:
        for sub in sub_dirs:
            path = folder + sub

            # skip directories which already exist
            if not os.path.isdir(path):
                os.mkdir(path)
                new_folders.append(path)

            # create ".keep" file to make git track the empty directory
            keep_path = path + "/.keep"
            if not os.path.isfile(keep_path):
                with open(keep_path, "w+") as file:
                    file.write("almost empty file to make git track the otherwise empty directory")
                new_files.append(keep_path)
                
    return new_folders, new_files

if __name__ == "__main__":
    source_dir = "data/source/"
    out = prepare_directories(source_dir)
    print(out)