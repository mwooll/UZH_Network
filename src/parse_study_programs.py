file_path = "data/text/HS24/VVZ_HS24_study_programs.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

print(content)



import re
import pandas as pd

# split stuff based on "Link:" there are 693 in total same as other keywords like ""Coordination:""
catalogs = re.split(r"\nLink:\s*\n", content)


course_data = []

for catalog in catalogs[1:]:
    catalog = catalog.strip()  
    if catalog:  
        # Extract the line after "Link:"
        program = re.search(r"^([^\n]+)", catalog)  # Capture the first line after "Link:"
        program = program.group(1).strip() if program else None

        # NOT NEEDED
        description = re.search(r"General description:\s*\n(.+?)(?:\nRequirements:)", catalog, re.DOTALL)
        description = description.group(1).strip().replace("\n", " ") if description else None

        admission = re.search(r"Admission Requirements:\s*\n(.+?)(?:\nParticulars/Requirements:)", catalog, re.DOTALL)
        admission = admission.group(1).strip().replace("\n", " ") if admission else None
        
        particulars = re.search(r"Particulars/Requirements:\s*\n(.+?)(?:\nRegulations:)", catalog, re.DOTALL)
        particulars = particulars.group(1).strip().replace("\n", " ") if particulars else None


        # can be multiple languages "Spanish, Portoguese" separated by comma
        languages = re.search(r"Languages of Instruction:\s*(.+)", catalog)
        languages = languages.group(1).strip() if languages else None

        # can be either https or http
        regulations = re.search(r"Regulations:\s*(https?://\S+)", catalog)
        regulations = regulations.group(1).strip() if regulations else None

        # there is a "Organization:" header without anything after it so make " " space to get the second one
        organization = re.search(r"Organization: (.*)", catalog)
        organization = organization.group(1).strip() if organization else None
        organization = organization if len(organization) >1 else None
        # ": " space to be sure, on the same line
        responsible = re.search(r"Responsible Instructor: (.*)", catalog)
        responsible = responsible.group(1).strip() if responsible else None
        responsible = responsible if len(responsible) >1 else None
        # on the same line
        coordination = re.search(r"Coordination: (.*)", catalog)
        coordination = coordination.group(1).strip() if coordination else None
        coordination = coordination if len(coordination) >1 else None
        #  Part Of: All lines after it, until we reach "course Catalog" ignore Page 1 of 1
        part_of = re.findall(r"Part of:\s*\n(.+?)(?=\nPage \d+ of \d+|$)", catalog, re.DOTALL)
        part_of = part_of[0].strip().replace("\n", "; ") if part_of else None

        # make dic
        course_data.append({
            "Program": program,
            # "General Description": description,
            "Languages": languages,
            # "Admission Requirements": admission,
            # "Particular Requirements": particulars,
            "Regulations": regulations,
            "Organization": organization,
            "Responsible Instructor": responsible,
            "Coordination": coordination,
            "Part Of": part_of
        })


df = pd.DataFrame(course_data)
# df.to_csv("../data/csv/VZZ_HS24_study_programs.csv", index=False)

# expected number of rows
num_rows = len(df)
if num_rows == 693:
    print(f"Success! The dataset contains the expected 693 rows.")
else:
    print(f"Warning: The dataset contains {num_rows} rows instead of 693.")

print("Processed data saved to 'course_catalog.csv'")
