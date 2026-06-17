import urllib.request
import re

def check_page():
    url = "https://insure153.com/1-3%ec%a2%85-%ec%88%98%ec%88%a0-%eb%b6%84%eb%a5%98%ed%91%9c/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        print("1-3 Page HTML Length:", len(html))
        
        tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
        print(f"Found {len(tables)} tables")
        
        # Print table snippets
        for idx, t in enumerate(tables):
            print(f"Table {idx+1} length: {len(t)}")
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.DOTALL)
            print(f"Table {idx+1} rows: {len(rows)}")
            for r_idx, r in enumerate(rows[:3]):
                cols = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL)
                cols_clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cols]
                print(f"  Row {r_idx+1}: {cols_clean}")
                
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    check_page()
