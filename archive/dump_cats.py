import json

with open(r'c:\Users\SB\Desktop\연습용\mcbride_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open(r'c:\Users\SB\Desktop\연습용\categories.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(d):
        out.write(f"Sheet {i+1}: {item['major']} - {item['minor']}\n")
