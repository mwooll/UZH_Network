import csv
import fitz 
import os
import pandas as pd
import re

def extract_module_components(source_dir, print_dir):
    programs = f"{print_dir}HS24/VVZ_HS24_study_programs.csv"
    abbr_length = 12
    deg_abbrs = set(get_list_of_degree_abbreviations(programs, abbr_length))
    print(deg_abbrs)

    new_files = []
    for semester in ["FS23", "HS23", "FS24", "HS24"]:
        pdf_file = f"{source_dir}{semester}/VVZ_{semester}_modules.pdf"
        out_file = f"{print_dir}{semester}/VVZ_{semester}_module_components.csv"
        scrape_components(pdf_file, out_file, deg_abbrs, abbr_length)
        new_files.append(out_file)
    return new_files

def get_list_of_degree_abbreviations(csv_file, abbr_length):
    df = pd.read_csv(csv_file, encoding="utf-16")
    degrees = df["Part Of"]
    return [degree[:abbr_length] for degree in degrees]

def scrape_components(pdf_file, out_file, degrees, abbr_length):
    results = []
    pdf = fitz.open(pdf_file)
    page_counter = 0
    length = len(pdf)
    while page_counter < length:
        page = pdf[page_counter]
        string = page.get_text("text")
       
        module, num_pages = find_module_name_and_num_pages(string)
        # print(module, num_pages)
        components = get_components(pdf[page_counter : page_counter + num_pages], degrees, abbr_length)
        results.append({"Module": module, "Components": components})

        page_counter += num_pages
        # if page_counter >= 600:
        #     break

    pdf.close()
    # print(results)
    with open(out_file, mode="w", newline="", encoding="utf-16") as file:
        writer = csv.DictWriter(file, fieldnames=["Module", "Components"])
        writer.writeheader()
        writer.writerows(results)


def get_components(pages, degrees, abbr_length):
    # print(len(pages))
    components = []
    find_start = True

    study_area = None
    for page in pages:
        dict = page.get_text("dict")
        blocks = dict["blocks"]

        for block in blocks:
            if find_start:
                if "lines" in block.keys():
                    spans = block['lines']
                    for i_span, span in enumerate(spans):
                        data = span['spans']
                        for i_lines, lines in enumerate(data):
                            if "Component" in lines["text"][:13]:
                                find_start = False
                                if len(span["spans"]) > 1:
                                    study_area = data[-1]["text"]
                                    # print(f"len(span[spans]): {study_area}")
                                if len(spans) > 1:
                                    study_area = spans[-1]["spans"][0]["text"]
                                    # print(f"len(span): {study_area}")
                                

            else:
                if "lines" in block.keys():
                    spans = block['lines']
                    for span in spans:
                        data = span['spans']
                        for lines in data:
                            # print(lines["font"], lines["text"])
                            if lines["text"][:8] == "Courses:":
                                component_string = "; ".join(components)
                                return component_string
                            elif lines["text"][:5] == "Empty":
                                continue
                            elif "Bold" in lines["font"]:
                                study_area = lines["text"]
                                # print(study_area)
                            else:
                                if lines["text"][:5] in ("Singl", "Major", "Minor"):
                                    program = lines["text"]
                                elif lines["text"][:10] in ("Doctoral P", "Individual",
                                                            "Teaching S"):
                                    program = lines["text"]
                                elif lines["text"][:14] in ("Additional Tea"):
                                    program = lines["text"]
                                elif lines["text"][:abbr_length] in degrees:
                                    try:
                                        components.append(f"{program} {study_area}---{lines['text'].strip()}")
                                    except:
                                        print([lines["text"] for lines in data])


    component_string = "; ".join(components)
    return component_string


def find_module_name_and_num_pages(text):
    lines = text.split("\n")
    for line in lines:
        if "Page 1 of" in line[:9]:
            of_pages = line[10:]
            num_pages = int(of_pages) if of_pages else 1
                            
        if "Module" in line[:6]:
            module = line[7:]
            return module, num_pages


if __name__ == "__main__":
    new_files = extract_module_components("../ns_data_source/", "data/csv/")
    print(new_files)