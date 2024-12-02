from pypdf import PdfReader

file_name = "data/source/HS24/VVZ_HS24_modules.pdf"
reader = PdfReader(file_name)
print(f"reader for {file_name} is ready")

text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

txt_file = "data/text/HS24/VVZ_HS24_modules.txt"
with open(txt_file, "w+") as file_to_write:
    file_to_write.write(text)
print(f"{file_name} was read and written to {txt_file}")