import json
import re
import sys

with open('raw_js.txt', 'r', encoding='utf-8') as f:
    js_data = f.read()

# Let's search for "메리츠화재"
idx = js_data.find("메리츠화재")
if idx != -1:
    print("Found 메리츠화재 at", idx)
    print(js_data[max(0, idx-100):min(len(js_data), idx+500)])
else:
    print("NOT FOUND")
