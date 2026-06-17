import re
import sys

try:
    # Try reading as UTF-8 first
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    encoding_used = 'utf-8'
except UnicodeDecodeError:
    # Fallback to CP949
    with open('index.html', 'r', encoding='cp949') as f:
        html = f.read()
    encoding_used = 'cp949'

# Find the input tag and replace its placeholder
pattern = re.compile(r'(<input[^>]*id="kcd-search-input"[^>]*placeholder=")([^"]*)(")', re.IGNORECASE)

def replace_placeholder(match):
    return match.group(1) + '질병코드 또는 질병명을 입력하세요' + match.group(3)

new_html, count = pattern.subn(replace_placeholder, html)

if count > 0:
    with open('index.html', 'w', encoding=encoding_used) as f:
        f.write(new_html)
    print(f"Successfully updated placeholder. Replaced {count} occurrences. Encoding used: {encoding_used}")
else:
    print("Could not find the placeholder to replace. Searching line by line:")
    for i, line in enumerate(html.split('\n')):
        if 'kcd-search-input' in line:
            print(f"Line {i+1}: {line.strip()}")
