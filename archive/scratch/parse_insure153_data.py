import urllib.request
import re
import json

def find_data():
    url = "https://insure153.com/%ec%88%98%ec%88%a0%eb%aa%85-%ea%b2%80%ec%83%89/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        print("Page HTML Length:", len(html))
        
        # Save HTML for inspection
        with open("scratch/insure153_search.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        # Search for TablePress or table data or large JSON arrays
        # Check if there are tables in HTML
        tables = re.findall(r'<table[^>]*>', html)
        print(f"Found {len(tables)} table tags")
        
        # Check if there's TablePress data
        tablepress = re.findall(r'tablepress', html, re.IGNORECASE)
        print(f"TablePress occurrences: {len(tablepress)}")
        
        # Check for large JSON or script data
        # Find all script contents
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
        print(f"Found {len(scripts)} inline script tags")
        for i, s in enumerate(scripts):
            s_len = len(s.strip())
            if s_len > 1000:
                print(f"Large Inline Script {i+1}: Length {s_len}")
                # Print first 200 chars and last 200 chars
                snippet = s.strip()
                print("Start:", snippet[:200])
                print("End:", snippet[-200:])
                
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    find_data()
