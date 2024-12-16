



import re
import pandas as pd



def process_hs24_study_programs(content):
    # Split the content based on "Course Catalog  "
    catalogs = re.split(r"Course Catalog\s+", content)

    # Initialize a list to store extracted data
    course_data = []

    # Process each catalog (skip the first empty split if present)
    for catalog in catalogs[1:]:
        catalog = catalog.strip()  
        if catalog:  
            # Extract the program name
            program = re.search(r"Link:\s*(.+)", catalog)
            program = program.group(1).strip() if program else None

            # Extract Languages of Instruction
            languages = re.search(r"Languages of Instruction:\s*(.+)", catalog)
            languages = languages.group(1).strip() if languages else None

            # Extract Regulations (URLs starting with http or https)
            regulations = re.search(r"Regulations:\s*(https?://\S+)", catalog)
            regulations = regulations.group(1).strip() if regulations else None

            # Extract Organization information
            organization = re.search(r"Organization: (.*)", catalog)
            organization = organization.group(1).strip() if organization else None
            organization = organization if len(organization) > 1 else None

            # Extract Responsible Instructor
            responsible = re.search(r"Responsible Instructor: (.*)", catalog)
            responsible = responsible.group(1).strip() if responsible else None
            responsible = responsible if len(responsible) > 1 else None

            # Extract Coordination details
            coordination = re.search(r"Coordination: (.*)", catalog)
            coordination = coordination.group(1).strip() if coordination else None
            coordination = coordination if len(coordination) > 1 else None

            # Extract "Part Of" section
            part_of = re.findall(r"Part of:\s*\n(.+?)(?=\nPage \d+ of \d+|$)", catalog, re.DOTALL)
            part_of = part_of[0].strip().replace("\n", "; ") if part_of else None

            # Append the extracted details as a dictionary
            course_data.append({
                "Program": program,
                "Languages": languages,
                "Regulations": regulations,
                "Organization": organization,
                "Responsible Instructor": responsible,
                "Coordination": coordination,
                "Part Of": part_of
            })

   
    df_result = pd.DataFrame(course_data)
    
    df_result['Part Of'] = df_result['Part Of'].apply(lambda x: ";".join([part.strip() for part in x.split(";") if "Page " not in part]) if pd.notnull(x) else x)

    
    return df_result



import pandas as pd
import re

def process_course_catalogs(file_content):
    catalogs = re.split(r"Course Catalog\s+", file_content)
    course_data = []
    
    # Process each catalog (skip the first empty split if present)
    for catalog in catalogs[1:]:
        catalog = catalog.strip()
        if catalog:
            # Extract the line after "Printing date" as the program name
            program_match = re.search(r"Printing date:\s*[^\n]*\n(.+)", catalog)
            program = program_match.group(1).strip() if program_match else None

            # Extract Languages of Instruction
            languages = re.search(r"Languages of Instruction: +([^\n]*)", catalog)
            languages = languages.group(1).strip() if languages else None

            # Extract Regulations (URLs starting with http or https)
            regulations = re.search(r"Regulations:\s*(https?://\S+)", catalog)
            regulations = regulations.group(1).strip() if regulations else None

            # Extract Organization information
            organization = re.search(r"Organization: (.*)", catalog)
            organization = organization.group(1).strip() if organization else None
            organization = organization if len(organization) > 1 else None

            # Extract Responsible Instructor
            responsible = re.search(r"Responsible Instructor: (.*)", catalog)
            responsible = responsible.group(1).strip() if responsible else None
            responsible = responsible if len(responsible) > 1 else None

            # Extract Coordination details
            coordination = re.search(r"Coordination: (.*)", catalog)
            coordination = coordination.group(1).strip() if coordination else None
            coordination = coordination if len(coordination) > 1 else None

            # Extract "Part Of" section
            part_of = re.findall(r"Part of:\s*\n(.+?)(?=\nPage \d+ of \d+|$)", catalog, re.DOTALL)
            part_of = part_of[0].strip().replace("\n", "; ") if part_of else None

      
            course_data.append({
                "Program": program,
                "Languages": languages,
                "Regulations": regulations,
                "Organization": organization,
                "Responsible Instructor": responsible,
                "Coordination": coordination,
                "Part Of": part_of
            })
    df_result = pd.DataFrame(course_data)
    df_result['Part Of'] = df_result['Part Of'].apply(lambda x: ";".join([part.strip() for part in x.split(";") if "Page " not in part]) if pd.notnull(x) else x)
    return df_result


import os


def get_semester_name(file_path):
    return os.path.basename(file_path).split("_")[1]



def save_data_csv(semester_name, df_result):
    csv_dir = f"data/csv/{semester_name}"
    os.makedirs(csv_dir, exist_ok=True)  
    csv_path = os.path.join(csv_dir, f"VVZ_{semester_name}_study_programs.csv")
    df_result.to_csv(csv_path, index=False, encoding="utf-16")
    
if __name__=="__main__":
    file_paths = ["data/text/FS24/VVZ_FS24_study_programs.txt", "data/text/FS23/VVZ_FS23_study_programs.txt", "data/text/HS23/VVZ_HS23_study_programs.txt"]
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            file_content = file.read()
        df_result = process_course_catalogs(file_content)
        semester_name = get_semester_name(file_path)
        save_data_csv(semester_name, df_result)
 
    file_path = "data/text/HS24/VVZ_HS24_study_programs.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        df_result = process_hs24_study_programs(content)
        semester_name = get_semester_name(file_path)
        save_data_csv(semester_name, df_result)
    