import pdfplumber

pdf_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part2.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[6] # Page 7
    words = page.extract_words()
    max_x = max(w['x1'] for w in words)
    min_x = min(w['x0'] for w in words)
    
    # We add lines to the left and right edges
    ts = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "explicit_vertical_lines": [min_x - 5, max_x + 5],
        "intersection_x_tolerance": 20,
        "intersection_y_tolerance": 20,
    }
    
    tables = page.extract_tables(table_settings=ts)
    if tables:
        for row in tables[0][:15]: # Print first 15 rows
            print([c.replace('\n', '') if c else '' for c in row])
