import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/parsed_latest.txt', 'r', 'utf-8').read().splitlines()

# find headers
headers = []
for i, line in enumerate(text):
    if line.strip() in ['총칙', '장해의 분류', '지급률', '<부표>'] or re.match(r'^\d+\.\s+.*장해.*', line) or line.strip() == '1. 눈의 장해':
        headers.append((i, line.strip()))

with open('c:/Users/SB/Desktop/연습용/dump_headers.txt', 'w', encoding='utf-8') as f:
    for h in headers:
        f.write(f"{h[0]}: {h[1]}\n")
