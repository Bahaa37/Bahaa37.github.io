import sys
from pypdf import PdfReader

path = r"C:\Users\bahaa\OneDrive\Desktop\My Resume Project\resume 2-9-26.pdf"
reader = PdfReader(path)
print("PAGES:", len(reader.pages))
for i, page in enumerate(reader.pages):
    print(f"\n===== PAGE {i+1} =====")
    print(page.extract_text())
