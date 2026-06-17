import codecs
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8').read()

# Locate v9502_life_9901
start_idx = script.find('v9502_life_9901: {')
if start_idx == -1:
    print("Could not find v9502_life_9901")
    exit()

# It is the last object in allDisabilityData, which ends with "\n};"
end_idx = script.find('\n};', start_idx)
if end_idx == -1:
    print("Could not find end of allDisabilityData")
    exit()

v9502_text = script[start_idx:end_idx]

# 1. Add type: 'tab'
if 'type: "tab"' not in v9502_text and "type: 'tab'" not in v9502_text:
    v9502_text = v9502_text.replace('v9502_life_9901: {', 'v9502_life_9901: {\n        type: "tab",')

# 2. Rename grade to category
v9502_text = re.sub(r'grade:\s*"(\d+)급"', r'category: "제\1급"', v9502_text)

# 3. Convert string items to objects in grades and parts
lines = v9502_text.split('\n')
new_lines = []
current_rate = ""
in_parts = False
in_explanations = False

for line in lines:
    cat_match = re.search(r'category:\s*"(제\d+급)"', line)
    if cat_match:
        current_rate = cat_match.group(1)[1:] # "1급"
    
    if 'parts:' in line:
        in_parts = True
        
    if 'explanations:' in line:
        in_explanations = True
        in_parts = False

    if not in_parts and not in_explanations:
        item_match = re.match(r'^(\s*)"(\d+\.\s+.*?)"(,?)\s*$', line)
        if item_match:
            indent, desc, comma = item_match.groups()
            new_lines.append(f'{indent}{{ desc: "{desc}", rate: "{current_rate}" }}{comma}')
            continue
            
    if in_parts and not in_explanations:
        item_match = re.match(r'^(\s*)"(\d+\.\s+.*?)\s*\((\d+급)\)"(,?)\s*$', line)
        if item_match:
            indent, desc, rate, comma = item_match.groups()
            new_lines.append(f'{indent}{{ desc: "{desc}", rate: "{rate}" }}{comma}')
            continue
            
    new_lines.append(line)

new_v9502 = '\n'.join(new_lines)
script = script[:start_idx] + new_v9502 + script[end_idx:]

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8').write(script)
print("v9502_life_9901 reformatted successfully!")
