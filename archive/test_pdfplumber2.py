import pdfplumber
import json

pdf_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part2.pdf"

def test_extract(page_num):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1]
        
        # Determine the rightmost edge of the text
        words = page.extract_words()
        max_x = max(w['x1'] for w in words) if words else page.width
        
        # We need to add an explicit vertical line at the right edge
        # pdfplumber table extraction uses lines. We can just add a line to explicit_vertical_lines.
        
        ts = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "explicit_vertical_lines": [max_x + 5],
            "intersection_x_tolerance": 20,
            "intersection_y_tolerance": 20,
        }
        
        tables = page.extract_tables(table_settings=ts)
        if tables:
            print(f"--- Page {page_num} Extracted ---")
            for row in tables[0][:2]:
                print([c.replace('\n', '') if c else '' for c in row])

test_extract(3)
test_extract(7)
test_extract(10)
