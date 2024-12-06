import os

from pypdf import PdfReader

def write_pdf_to_text(file_path):
    output_file = file_path.replace("source", "text").replace(".pdf", ".txt")
    if os.path.isfile(output_file):
        return

    print(f"reading: {file_path}; will write to {output_file}")
    reader = PdfReader(file_path)

    with open(output_file, "w+") as file_to_write:
        for page in reader.pages:
            page_content = page.extract_text()
            file_to_write.write(page_content + "\n")

    return output_file


def convert_pdfs_to_txt(source_dir): 
    new_files = []
    for path, dirs, files in os.walk(source_dir):
        for file in files:
            if "Zone.Identifier" in file:
                continue

            filename = path + "/" + file
            out = write_pdf_to_text(filename)
            if out:
                new_files.append(out)
    return new_files


if __name__ == "__main__":
    source_dir = "data/source"
    new_files = convert_pdfs_to_txt(source_dir)
    print(new_files)
