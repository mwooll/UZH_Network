import re
import pandas as pd
from datetime import datetime

def extract_event_data(text):
    # Search patterns
    event_name_pattern = r"Event (.+)"
    event_code_pattern = r"([A-Za-z0-9._-]+) /"
    event_type_pattern = r"[A-Za-z0-9._-]+ / (.+?) /"
    instructor_pattern = r"Instructor: (.+?)\nLanguages"
    languages_pattern = r"Languages: (.+)"
    component_of_module_pattern = r"Module: (.+)"
    time_pattern = r"(\w{3} \d{1,2}, \d{4}) (\d{1,2}:\d{2}) - (\d{1,2}:\d{2})"

    events = []

    # Split the text into module blocks based on "Printing Date"
    module_blocks = re.split(r"Printing Date:", text)

    for block in module_blocks:
        # Match the patterns
        event_name_match = re.search(event_name_pattern, block)
        event_code_match = re.search(event_code_pattern, block)
        event_type_match = re.search(event_type_pattern, block)
        instructor_match = re.search(instructor_pattern, block, re.DOTALL)
        languages_match = re.search(languages_pattern, block)
        component_of_module_match = re.search(component_of_module_pattern, block)

        # Extract all time matches
        time_matches = re.findall(time_pattern, block)

        # Extract the first date and time if present
        if time_matches:
            first_date, start_time, _ = time_matches[0]  # Use the first match
            # Convert date to weekday
            weekday = datetime.strptime(first_date, "%b %d, %Y").strftime("%A")
            # Classify daytime
            hour = int(start_time.split(":")[0])
            if 6 <= hour < 12:
                daytime = "Morning"
            elif 12 <= hour < 18:
                daytime = "Afternoon"
            else:
                daytime = "Evening"
        else:
            weekday = "N/A"
            daytime = "N/A"

        # Extract and clean up other data
        event_name = event_name_match.group(1).strip() if event_name_match else "N/A"
        event_code = event_code_match.group(1).strip() if event_code_match else "N/A"
        event_type = event_type_match.group(1).strip() if event_type_match else "N/A"
        instructors = instructor_match.group(1).replace("\n", ", ").strip() if instructor_match else "N/A"
        languages = languages_match.group(1).strip() if languages_match else "N/A"
        component_of_module = component_of_module_match.group(1).strip() if component_of_module_match else "N/A"

        # Append the data to the list
        events.append({
            "Event Name": event_name,
            "Event Code": event_code,
            "Event Type": event_type,
            "Instructor": instructors,
            "Course Languages": languages,
            "Component of Module": component_of_module,
            "Weekday": weekday,
            "Daytime": daytime
        })

    return events

def main(input_file, output_file):
    # Read the input text file
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Apply function
    event_data = extract_event_data(text)
    
    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(event_data)
    df.to_csv(output_file, index=False)
    print(f"CSV file saved at: {output_file}")

# Usage example
semesters = ['FS23', 'HS23', 'FS24', 'HS24']

for semester in semesters:
    input_file = f"data/text/{semester}/VVZ_{semester}_time_schedules.txt"  
    output_file = f"data/csv/{semester}/VVZ_{semester}_time_schedule.csv"  
    main(input_file, output_file)
