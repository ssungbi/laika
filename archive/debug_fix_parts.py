import codecs
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

start_idx = script.find('"v9902_life": {')
end_idx = script.find('v9502_life_9901: {')

v9902_text = script[start_idx:end_idx]

parts_start = v9902_text.find('parts: [')
parts_end = v9902_text.find('explanations: [', parts_start)

if parts_start != -1 and parts_end != -1:
    parts_text = v9902_text[parts_start:parts_end]
    
    matches = list(re.finditer(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', parts_text))
    print(f"Found {len(matches)} matches")
    for m in matches[:5]:
        print(m.groups())
else:
    print("Could not find parts or explanations")
