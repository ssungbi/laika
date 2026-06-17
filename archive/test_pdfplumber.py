import pdfplumber
import json

pdf_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part2.pdf"

def test_extract(page_num):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1]
        
        print(f"--- Page {page_num} Text Settings ---")
        ts = {
            "vertical_strategy": "text",
            "horizontal_strategy": "text"
        }
        tables2 = page.extract_tables(table_settings=ts)
        if tables2:
            print([c.encode('unicode_escape').decode() if c else c for c in tables2[0][0]])

test_extract(3)
test_extract(7)
