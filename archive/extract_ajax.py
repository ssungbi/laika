import re
import json

with open('kcd9.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for jQuery $.ajax or $.get or fetch
print("AJAX CALLS:")
for m in re.finditer(r'(?:ajax|get|post)\s*\(\{([^\}]+)\}', html, re.IGNORECASE):
    print(m.group(1).strip()[:100])

# Look for variable declarations that might hold the tree data
print("\nTREE DATA:")
for m in re.finditer(r'var\s+\w+\s*=\s*\[\{.*?\}\]', html, re.DOTALL):
    print("Found array:", m.group(0)[:100])

# Just extract script tags
scripts = re.findall(r'<script.*?>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
for i, s in enumerate(scripts):
    if 'koicd' in s.lower() or 'jstree' in s.lower() or 'ajax' in s.lower() or 'kcd' in s.lower():
        print(f"\nScript {i} (len={len(s)}):")
        print(s[:500])
