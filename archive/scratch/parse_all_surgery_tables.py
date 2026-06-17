import urllib.request
import re
import json
import os

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return text.strip()

def parse_table_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        # Find table
        tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
        if not tables:
            print(f"No tables found on {url}")
            return []
            
        data = []
        for table_idx, table_content in enumerate(tables):
            # We want TablePress tables (or the largest table)
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_content, re.DOTALL)
            parsed_rows = []
            for r in rows:
                cols = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL)
                cols_clean = [clean_html(c) for c in cols]
                if cols_clean:
                    parsed_rows.append(cols_clean)
            data.append(parsed_rows)
            
        # Return the largest table parsed
        if data:
            data.sort(key=len, reverse=True)
            return data[0]
        return []
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return []

def main():
    os.makedirs("scratch", exist_ok=True)
    
    # 1. Parse search page data
    print("Fetching and parsing surgery search page...")
    search_url = "https://insure153.com/%ec%88%98%ec%88%a0%eb%aa%85-%ea%b2%80%ec%83%89/"
    search_data = parse_table_from_url(search_url)
    if search_data:
        # Format: [ [name, grade_1_3, grade_1_5], ... ]
        # Skip header row if it exists
        header = search_data[0]
        rows = search_data[1:]
        print(f"Parsed {len(rows)} search rows. Header: {header}")
        
        out_path = "scratch/surgery_search_data.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"header": header, "rows": rows}, f, ensure_ascii=False, indent=2)
        print(f"Saved to {out_path}")
        
    # 2. Parse 1-3 types data
    print("Fetching and parsing 1-3 types page...")
    url_13 = "https://insure153.com/1-3%ec%a2%85-%ec%88%98%ec%88%a0-%eb%b6%84%eb%a5%98%ed%91%9c/"
    data_13 = parse_table_from_url(url_13)
    if data_13:
        header = data_13[0]
        rows = data_13[1:]
        print(f"Parsed {len(rows)} rows for 1-3 table. Header: {header}")
        
        out_path = "scratch/surgery_13_data.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"header": header, "rows": rows}, f, ensure_ascii=False, indent=2)
        print(f"Saved to {out_path}")
        
    # 3. Parse 1-5 types data
    print("Fetching and parsing 1-5 types page...")
    url_15 = "https://insure153.com/1-5%ec%a2%85-%ec%88%98%ec%88%a0-%eb%b6%84%eb%a5%98%ed%91%9c/"
    data_15 = parse_table_from_url(url_15)
    if data_15:
        header = data_15[0]
        rows = data_15[1:]
        print(f"Parsed {len(rows)} rows for 1-5 table. Header: {header}")
        
        out_path = "scratch/surgery_15_data.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"header": header, "rows": rows}, f, ensure_ascii=False, indent=2)
        print(f"Saved to {out_path}")

if __name__ == '__main__':
    main()
