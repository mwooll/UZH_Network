import os
import csv
from pathlib import Path

# possible header for final csv
csv_header = ["Name", "Number", "Type", "ECTS", "Language", "Responsible Instructor",
              "Prerequisites", "Prior Knowledge", "Component"]

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
                    # found a file we need to convert to csv

                convert_txt_to_csv(txt_file, csv_file)
                new_files.append(csv_file)

    return new_files

def convert_txt_to_csv(txt_file, csv_file):
    text = Path(txt_file).read_text()

    # a new module always starts with "Page 1", the very first entry is empty
    modules = text.split("Page 1")[1:]

    extract_fields_from_modules(modules[:1])

    data = {}
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Responsible", "Prerequisites"])
        writer.writeheader()
        writer.writerows(data)

def extract_fields_from_modules(modules):
    results = []
    for module in modules:
        print(module)
        module_info = {}
        lines = module.split("\n")

        for line in lines:
            if "Responsible instructor:" in line:
                instructor = line.split("Responsible instructor:")[-1].strip()
                
                instructor_name = instructor.split("Requirements")[0].strip()
                module_info["Responsible Instructor"] = instructor_name
                break
    
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
    
        if module_info:  
            results.append(module_info)
        
    return results


if __name__ == "__main__":
    txt_directory = "data/text/HS24/"
    new = parse_modules(txt_directory)
    print(new)
