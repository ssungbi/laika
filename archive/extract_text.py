import pdfplumber

pdf_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part2.pdf"

with pdfplumber.open(pdf_path) as pdf:
    text3 = pdf.pages[2].extract_text() or ""
    text7 = pdf.pages[6].extract_text() or ""
    text10 = pdf.pages[9].extract_text() or ""
    text15 = pdf.pages[14].extract_text() or ""
    text19 = pdf.pages[18].extract_text() or ""
    text20 = pdf.pages[19].extract_text() or ""

with open("pdf_text.txt", "w", encoding="utf-8") as f:
    f.write(f"--- Page 3 ---\n{text3}\n")
    f.write(f"--- Page 7 ---\n{text7}\n")
    f.write(f"--- Page 10 ---\n{text10}\n")
    f.write(f"--- Page 15 ---\n{text15}\n")
    f.write(f"--- Page 19 ---\n{text19}\n")
    f.write(f"--- Page 20 ---\n{text20}\n")
