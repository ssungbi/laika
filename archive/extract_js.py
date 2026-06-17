import re

with open('kcd9.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*src=[\'\"]([^\'\"]+)[\'\"]', html)
for s in scripts:
    print(s)
