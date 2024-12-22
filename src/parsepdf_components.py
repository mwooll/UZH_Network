import fitz 
import pandas as pd
import re

def extract_data_from_pdf(pdf_path, output_csv):
    doc = fitz.open(pdf_path)
    extracted_data = []
    current_table_name = None
    last_valid_table_name = None  
    capture_next_line = False

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text = page.get_text("text")
        lines = text.split("\n")

        for i, line in enumerate(lines):
            line = line.strip()

            # Checking for "Component of" -- Rn working only for the 1st
            if "Component of" in line:
                possible_name = line.replace("Component of:", "").strip()
                if possible_name and possible_name != "Empty":
                    current_table_name = possible_name
                else:
                    capture_next_line = True

            elif capture_next_line:
                # for the non-empty
                if line and line != "Empty":  # consider only when its "Empty"
                    current_table_name = line
                    capture_next_line = False 
            
            if not current_table_name:
                current_table_name = last_valid_table_name
            else:
                last_valid_table_name = current_table_name

            # for fields  "Single Major 180," "Major 150,"...
            if current_table_name:
                match = re.findall(r'\b(Single Major \d{3}|Major \d{3}|Minor \d{2,3})\b', line, re.IGNORECASE)
                for field in match:
                    extracted_data.append([current_table_name, field])

    if extracted_data:
        df = pd.DataFrame(extracted_data, columns=["Table Name", "Field"])
        df.to_csv(output_csv, index=False)
        print(f"Data saved to {output_csv}")
    else:
        print("No matching data found.")

extract_data_from_pdf("/Users/akavas/Desktop/c_5.pdf", "output_components.csv")