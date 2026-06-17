import re
import urllib.request
import json

file_path = r"C:\Users\SB\.gemini\antigravity-ide\brain\e2b50c29-6ecb-4da1-ba61-8017d93522fc\.system_generated\steps\483\content.md"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

urls = set(re.findall(r'url\s*:\s*[\'\"]([^\'\"]+)[\'\"]', html))
print("Found URLs:", urls)

# Let's see if there's a JSON or API link like /api/kcd9/tree or something
for url in urls:
    if "api" in url or "json" in url or "get" in url.lower():
        print("Potential API:", url)

# Let's also search for 'chapter' or 'block' to see if data is embedded
blocks = re.findall(r'(\{[^\}]*chapter[^\}]*\})', html, re.IGNORECASE)
if blocks:
    print(f"Found {len(blocks)} blocks mentioning chapter.")
else:
    print("No embedded JSON blocks found for chapter.")
