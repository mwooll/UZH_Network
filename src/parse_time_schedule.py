import re
import pandas as pd

def extract_event_data(text):
    # search patterns
    event_name_pattern = r"Event (.+)"
    event_code_pattern = r"([A-Za-z0-9._-]+) /"
    instructor_pattern = r"Instructor: (.+)"
    languages_pattern = r"Languages: (.+)"
    component_of_module_pattern = r"Module: (.+)"
    
    events = []
    
    # blocks of modules at the beginning of each (page 1)
    module_blocks = re.split(r"Page 1 of \d+", text)
    
    for block in module_blocks:
        event_name_match = re.search(event_name_pattern, block)
        event_code_match = re.search(event_code_pattern, block)
        instructor_match = re.search(instructor_pattern, block)
        languages_match = re.search(languages_pattern, block)
        component_of_module_match = re.search(component_of_module_pattern, block)
        # extract and clean up
        event_name = event_name_match.group(1).strip() if event_name_match else "N/A"
        event_code = event_code_match.group(1).strip() if event_code_match else "N/A"
        instructor = instructor_match.group(1).strip() if instructor_match else "N/A"
        languages = languages_match.group(1).strip() if languages_match else "N/A"
        compentent_of_module = component_of_module_match.group(1).strip() if component_of_module_match else "N/A"
        
        #append
        events.append({
            "Event Name": event_name,
            "Event Code": event_code,
            "Instructor": instructor,
            "Course Languages": languages,
            "Component of Module": compentent_of_module
        })
    
    return events

def main(input_file, output_file):
    # read
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # apply function
    event_data = extract_event_data(text)
    
    df = pd.DataFrame(event_data)
    df.to_csv(output_file, index=False)
    print(f"CSV file saved at: {output_file}")



semesters = ['FS23','HS23','FS24','HS24']

for semester in semesters:

    input_file = f"data/text/{semester}/VVZ_{semester}_time_schedules.txt"  
    output_file = f"data/csv/{semester}/VZZ_{semester}_time_schedule.csv"  
    main(input_file, output_file)
