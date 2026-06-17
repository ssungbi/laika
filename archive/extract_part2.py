import pdfplumber
import json

pdf_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part2.pdf"

all_tables = []

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for t in tables:
            all_tables.append({
                "page": i + 1,
                "table": t
            })

with open("part2_tables.json", "w", encoding="utf-8") as f:
    json.dump(all_tables, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(all_tables)} tables from part2.pdf")
