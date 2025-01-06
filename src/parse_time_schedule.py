import re
import pandas as pd
from datetime import datetime

def extract_event_data(text):
    event_name_pattern = r"Event (.+)"
    event_code_pattern = r"([A-Za-z0-9._-]+) /"
    event_type_pattern = r"[A-Za-z0-9._-]+ / (.+?) /"
    instructor_pattern = r"Instructor: (.+?)\nLanguages"
    languages_pattern = r"Languages: (.+)"
    component_of_module_pattern = r"Module: (.+)"
    time_pattern = r"(\w{3} \d{1,2}, \d{4}) (\d{1,2}:\d{2}) - (\d{1,2}:\d{2})"

    events = []

    module_blocks = re.split(r"Printing Date:", text)

    for block in module_blocks:
        event_name_match = re.search(event_name_pattern, block)
        event_code_match = re.search(event_code_pattern, block)
        event_type_match = re.search(event_type_pattern, block)
        instructor_match = re.search(instructor_pattern, block, re.DOTALL)
        languages_match = re.search(languages_pattern, block)
        component_of_module_match = re.search(component_of_module_pattern, block)

        time_matches = re.findall(time_pattern, block)


        if time_matches:
            first_date, start_time, end_time = time_matches[0]  #sse the first match
            weekday = datetime.strptime(first_date, "%b %d, %Y").strftime("%A")
            start_time = int(start_time.split(":")[0]) + (int(start_time.split(":")[1])/60)
            end_time = int(end_time.split(":")[0]) + (int(end_time.split(":")[1])/60)

            if 6 <= start_time < 12:
                daytime = "Morning"
            elif 12 <= start_time < 18:
                daytime = "Afternoon"
            else:
                daytime = "Evening"
        else:
            weekday = "N/A"
            daytime = "N/A"
            start_time = "N/A"
            end_time = "N/A"

        event_name = event_name_match.group(1).strip() if event_name_match else "N/A"
        event_code = event_code_match.group(1).strip() if event_code_match else "N/A"
        event_type = event_type_match.group(1).strip() if event_type_match else "N/A"
        instructor = instructor_match.group(1).strip().replace("\n", ", ") if instructor_match else "N/A"
        languages = languages_match.group(1).strip() if languages_match else "N/A"
        component_of_module = component_of_module_match.group(1).strip() if component_of_module_match else "N/A"

        events.append({
            "Event Name": event_name,
            "Event Code": event_code,
            "Event Type": event_type,
            "Instructor": instructor,
            "Course Languages": languages,
            "Component of Module": component_of_module,
            "Weekday": weekday,
            "Daytime": daytime,
            "Start Time": start_time,
            "End Time": end_time
        })


    return events

def main(input_file, output_file):

    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    event_data = extract_event_data(text)

    df = pd.DataFrame(event_data)
    df.to_csv(output_file, index=False)
    print(f"CSV file saved at: {output_file}")

semesters = ['FS23', 'HS23', 'FS24', 'HS24']

for semester in semesters:
    input_file = f"data/text/{semester}/VVZ_{semester}_time_schedules.txt"  
    output_file = f"data/csv/{semester}/VVZ_{semester}_time_schedule.csv"  
    main(input_file, output_file)
