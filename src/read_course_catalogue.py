import os

from pypdf import PdfReader

def write_pdf_to_text(file_path):
    reader = PdfReader(file_path)

    output_file = file_path.replace({"source": "text", ".pdf": ".txt"})
    print(output_file)
    
    with open(output_file, "w+") as file_to_write:
        for page in reader.pages:
            page_content = page.extract_text()
            file_to_write.write(page_content + "\n")

    return output_file


def convert_pdfs_to_txt(): 
    source_dir = "data/source"
    
    files_written = []
    for path, dirs, files in os.walk(source_dir):
        for file in files:
            filename = path + "/" + file
            out = write_pdf_to_text(filename)
            files_written.append(out)
    return files_written

if __name__ == "__main__":
    written_files = convert_pdfs_to_txt()
    print(written_files)