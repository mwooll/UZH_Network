import os
import csv
from pathlib import Path

# possible header for final csv
csv_header = ["Name", "Faculty", "Number", "Type", "ECTS", "Language", "Responsible instructor",
              "Prerequisites", "Prior Knowledge", "Component"]

# dictionairy with known faculties
faculties = {"01SM": "THF", "02SM": "RWF", "03SM": "WWF", "04SM": "MEF",
             "05SM": "VSF", "06SM": "PHF", "07SM": "MNF",
             "10SM": "Transdisciplinary Studies", "30SM": "Sprachkurs",
             # from now on: huh?
             "00UF": "",  "05DP": "", "04VL": "", "10_1": ""}

def parse_modules(txt_dir):
    new_files = []

    # parse the given directory
    for path, dirs, files in os.walk(txt_dir):
        for file in files:
            # search for the right files
            if "modules" in file:
                txt_file = path + "/" + file 
                csv_file = txt_file.replace("text", "csv").replace(".txt", ".csv")
                # skip files which have already been converted to csv
                # if not os.path.isfile(csv_file):
                convert_txt_to_csv(txt_file, csv_file)
                new_files.append(csv_file)

    return new_files

def convert_txt_to_csv(txt_file, csv_file):
    text = Path(txt_file).read_text()

    # a new module always starts with "Page 1", the very first entry is empty
    modules = text.split("Page 1")[1:]

    data = extract_fields_from_modules(modules)

    # need utf-16 for "üöä" not included in utf-8
    with open(csv_file, mode="w", newline="", encoding="utf-16") as file:
        writer = csv.DictWriter(file, fieldnames=csv_header)
        writer.writeheader()
        writer.writerows(data)

def extract_fields_from_modules(modules):
    results = []

    for module in modules:
        module_info = {}

        lines = module.split("\n")

        # find name of module
        for index, line in enumerate(lines):
            if line[:7] == "Module ":
                module_info["Name"] = line[7:]
                break

        # if we find no name, we can't continue
        if "Name" not in module_info:
            continue

        # can ignore if more than 2 values are returned from the split
        module_number, module_type = lines[index+1].split(" / ")[:2]
        lines = lines[index+2:]

        faculty, number = module_number[:4], module_number[4:]
        module_info["Faculty"] = faculties[faculty]
        module_info["Number"] = number
        module_info["Type"] = module_type

        # needs to be ordered as occurring in file
        simple_fields = ["ECTS", "Responsible instructor"]
        lines, module_info = find_one_line_fields(lines, simple_fields, module_info)
    
        for line in lines:
            if "Prerequisites:" in line:
                prerequisites = line.split("Prerequisites:")[-1].strip()
                stop_keywords = ["Assessment:", "Grading Scale:", "Repeatability:", "Organisation:"]
                for keyword in stop_keywords:
                    if keyword in prerequisites:
                        prerequisites = prerequisites.split(keyword)[0].strip()
                        break
                
                module_info["Prerequisites"] = prerequisites
                break

        # print(module_info)
        if module_info:  
            results.append(module_info)
        
    return results

def find_one_line_fields(lines, keywords, module_info):
    for word in keywords:
        length = len(word)
        for index, line in enumerate(lines):
            if line[:length] == word:
                # ignore ": "
                module_info[word] = line[length+2:]
                break
        lines = lines[index:]
    return lines, module_info


if __name__ == "__main__":
    txt_directory = "data/text/HS24/"
    new = parse_modules(txt_directory)
    print(new)
