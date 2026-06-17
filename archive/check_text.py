import pdfplumber

pdf_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part2.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print("--- Page 3 ---")
    print(pdf.pages[2].extract_text()[:500])
    print("--- Page 7 ---")
    print(pdf.pages[6].extract_text()[:500])
    print("--- Page 10 ---")
    print(pdf.pages[9].extract_text()[:500])
