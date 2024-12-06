

import csv
from PyPDF2 import PdfReader

def extract_responsible_and_prerequisites(pdf_path):
    reader = PdfReader(pdf_path)
    results = []
    for page in reader.pages:
        text = page.extract_text()

        modules = text.split("Module")
        for module in modules[1:]: 
            module_info = {}
            lines = module.split("\n")
            
            for line in lines:
                if "Responsible instructor:" in line:
                    instructor = line.split("Responsible instructor:")[-1].strip()
                    
                    instructor_name = instructor.split("Requirements")[0].strip()
                    module_info["Responsible"] = instructor_name
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

def save_to_csv(data, output_file):
    if not data:
        print("No data to write to CSV.")
        return

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Responsible", "Prerequisites"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Data successfully saved to {output_file}")

pdf_path = "/Users/akavas/Desktop/copy.pdf"  # I have taken the first 20 pages
output_csv = "responsible_and_prerequisites.csv"

extracted_data = extract_responsible_and_prerequisites(pdf_path)
save_to_csv(extracted_data, output_csv)