import json

with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('"name": "수협"')
if start_idx != -1:
    print(content[start_idx:start_idx+300])
else:
    print("수협 not found")
