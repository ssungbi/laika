import urllib.request
import re

def get_scripts():
    url = "https://insure153.com/%ec%88%98%ec%88%a0%eb%aa%85-%ea%b2%80%ec%83%89/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        print("Page HTML fetched successfully. Length:", len(html))
        # Find all script src tags
        scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
        for idx, src in enumerate(scripts):
            print(f"Script {idx+1}: {src}")
            
    except Exception as e:
        print("Error fetching URL:", e)

if __name__ == '__main__':
    get_scripts()
