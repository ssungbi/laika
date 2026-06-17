import os
import re

def extract_tables():
    html_path = "scratch/insure153_search.html"
    if not os.path.exists(html_path):
        print("HTML file not found")
        return
        
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Find all table content
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
    print(f"Extracted {len(tables)} tables")
    
    for idx, table_content in enumerate(tables):
        print(f"\n--- TABLE {idx+1} (Length: {len(table_content)}) ---")
        # Find rows
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_content, re.DOTALL)
        print(f"Number of rows: {len(rows)}")
        # Print first 3 rows as text snippets
        for r_idx, r in enumerate(rows[:5]):
            cols = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL)
            cols_clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cols]
            print(f"Row {r_idx+1}: {cols_clean}")

if __name__ == '__main__':
    extract_tables()
