import csv
import fitz
import pandas as pd


def extract_module_components(source_dir, print_dir):
    semesters = ["FS23", "HS23", "FS24", "HS24"]

    new_files = []
    for semester in semesters:
        # print(semester)
        degrees = get_degrees(print_dir, semester)
        pdf_file = f"{source_dir}/{semester}/VVZ_{semester}_modules.pdf"
        out_file = f"{print_dir}/{semester}/VVZ_{semester}_module_components.csv"
        scrape_components(pdf_file, out_file, degrees)
        new_files.append(out_file)
    return new_files


def get_degrees(print_dir, semester):
    def read_file(file_name):
        try:
            df = pd.read_csv(file_name, encoding="utf-16")
        except:
            df = pd.read_csv(file_name, encoding="utf-8")
        return df

    column_values = tuple()

    df = read_file(f"{print_dir}/{semester}/VVZ_{semester}_study_programs.csv")
    column_values += tuple(df["Part Of"])

    programs = []
    for column in column_values:
        for program in column.split(";"):
            programs.append(program.strip().replace("'", "").replace('"', ''))
    programs = sorted(list(set(programs)))
    return programs

def scrape_components(pdf_file, out_file, degrees):
    results = []
    pdf = fitz.open(pdf_file)
    page_counter = 0
    length = len(pdf)
    while page_counter < length:
        page = pdf[page_counter]
        string = page.get_text("text")
       
        module, num_pages = find_module_name_and_num_pages(string)
        components = get_components(pdf[page_counter : page_counter + num_pages], degrees)
        results.append({"Module": module, "Components": components})

        page_counter += num_pages

    pdf.close()
    with open(out_file, mode="w", newline="", encoding="utf-16") as file:
        writer = csv.DictWriter(file, fieldnames=["Module", "Components"])
        writer.writeheader()
        writer.writerows(results)


def get_components(pages, degrees):
    components = []
    find_start = True

    study_area = None
    program = None
    degree = None
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
                                    study_area = data[-1]["text"].replace('"', "")
                                if len(spans) > 1:
                                    study_area = spans[-1]["spans"][0]["text"].replace('"', "")
                                

            else:
                if "lines" in block.keys():
                    spans = block['lines']
                    for span in spans:
                        data = span['spans']
                        for lines in data:
                            if lines["text"][:8] == "Courses:":
                                component_string = ";;".join(set(components))
                                return component_string
                            elif lines["text"] in "Empty":
                                continue
                            elif "Bold" in lines["font"]:
                                study_area = lines["text"].replace('"', "")
                            else:
                                if lines["text"][:4] in ("Sing", "Majo", "Mino", "Area"):
                                    program = lines["text"]
                                elif lines["text"][:14] in ("Additional Tea", "Teaching Subje",
                                                            "Doctoral Progr", "Individual Doc"):
                                    program = lines["text"].replace('"', "")
                                else:
                                    degree = find_degree(lines["text"], degrees)
                                    if program and study_area and degree:
                                        components.append(f"{program} {study_area}---{degree}")
                                        program = None


    component_string = ";".join(components)
    return component_string

def find_degree(lines_text, degrees):
    if len(lines_text) <= 20:
        for deg in degrees:
            if lines_text == deg:
                return deg
    else:
        # some degrees have the exact length that it has problems finding the edges of cells...
        # also happens when searching in the pdf's
        for deg in ["BA UZH in Study of Religions Bologna 2020",
                    "Bachelor of Science in Psychology (RVO19)",
                    'Master of Arts in Social Sciences (RVO19)']:
            if deg in lines_text:
                return deg
        lines_text = lines_text.strip()
        for deg in degrees:
            if deg.startswith(lines_text):
                return deg
    return None

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
    new_files = extract_module_components("../ns_data_source", "data/csv")
    print(new_files)