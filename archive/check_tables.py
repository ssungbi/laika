import pdfplumber

pdf_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part2.pdf"

all_tables = []

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        words = page.extract_words()
        if not words:
            continue
            
        max_x = max(w['x1'] for w in words)
        min_x = min(w['x0'] for w in words)
        
        ts = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "explicit_vertical_lines": [min_x - 5, max_x + 5],
            "intersection_x_tolerance": 20,
            "intersection_y_tolerance": 20,
        }
        
        tables = page.extract_tables(table_settings=ts)
        for t in tables:
            all_tables.append({
                "page": i + 1,
                "header": t[0][:3] if len(t) > 0 else []
            })

for idx, t in enumerate(all_tables):
    print(f"Index: {idx}, Page: {t['page']}, Header: {t['header']}")
