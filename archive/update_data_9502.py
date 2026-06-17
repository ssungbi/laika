import codecs
import json
import re

# 1. Parse user_data_9502.txt
user_data = codecs.open('c:/Users/SB/Desktop/연습용/user_data_9502.txt', 'r', 'utf-8').read()

# split into grades and explanations
exp_start = user_data.find('장해등급분류 해설')
grades_text = user_data[:exp_start].strip()
exp_text = user_data[exp_start:].strip()

grades_9502 = []
current_grade = None

for line in grades_text.split('\n'):
    line = line.strip()
    if not line: continue
    
    m = re.match(r'^([1-6])급\s+(.*)', line)
    if m:
        current_grade = f"제{m.group(1)}급"
        grades_9502.append({"category": current_grade, "items": []})
        desc = m.group(2).strip()
        if desc and re.match(r'^\d+\.', desc):
            grades_9502[-1]['items'].append({"desc": desc, "rate": f"{m.group(1)}급"})
    elif current_grade and re.match(r'^\d+\.', line):
        grades_9502[-1]['items'].append({"desc": line, "rate": current_grade[-2:]})

# parse explanations for 9502
explanations_9502 = []
exp_blocks = re.split(r'\n(?=\d+\.\s+")', exp_text)
for block in exp_blocks:
    block = block.strip()
    if not block: continue
    m = re.match(r'\d+\.\s+"([^"]+)"\n(.*)', block, re.DOTALL)
    if m:
        explanations_9502.append({
            "title": m.group(1),
            "content": m.group(2).strip()
        })
    elif "장해등급분류 해설" not in block:
        # just in case
        lines = block.split('\n', 1)
        if len(lines) > 1:
            explanations_9502.append({
                "title": lines[0].strip(),
                "content": lines[1].strip()
            })

# 2. Extract v9902_life parts to build 9502 parts
script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
v9902_idx = script_text.find('"v9902_life": {')
parts_start = script_text.find('parts: [', v9902_idx)
exp_start2 = script_text.find('explanations: [', parts_start)

parts_text = script_text[parts_start:exp_start2]
# parse the parts text structure using a simple regex since it's well-formed
parts_data = []
categories = re.findall(r'\{\s*category:\s*"([^"]+)",\s*items:\s*\[(.*?)\](?:,\s*expIndices:\s*\[([\d,\s]*)\])?\s*\}', parts_text, re.DOTALL)

for cat, items_str, exp_str in categories:
    cat_items = []
    item_matches = re.findall(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', items_str)
    for desc, rate in item_matches:
        cat_items.append({"desc": desc, "rate": rate})
    
    exp_indices = [int(x.strip()) for x in exp_str.split(',')] if exp_str.strip() else []
    parts_data.append({"category": cat, "items": cat_items, "expIndices": exp_indices})

# Now map parts for 9502
# We match desc against grades_9502 items
def get_rate(desc, grades):
    clean_desc = re.sub(r'^\d+\.\s*', '', desc).strip()
    clean_desc = re.sub(r'<[^>]+>', '', clean_desc).strip()
    
    # fuzzy match
    from difflib import SequenceMatcher
    best_rate = "-"
    best_score = 0.8  # threshold
    for g in grades:
        for item in g['items']:
            g_desc = re.sub(r'^\d+\.\s*', '', item['desc']).strip()
            score = SequenceMatcher(None, clean_desc, g_desc).ratio()
            if score > best_score:
                best_score = score
                best_rate = f"{g['category'][-2:]}{item['desc'].split('.')[0]}항"
    return best_rate

for cat in parts_data:
    for item in cat['items']:
        item['rate'] = get_rate(item['desc'], grades_9502)

# Format parts
parts_json_str = json.dumps(parts_data, ensure_ascii=False, indent=12)
# The default json.dumps creates a huge string, let's just make it look somewhat nice
parts_json_str = parts_json_str.replace('\n            {', ' {').replace('\n            }', ' }')

# 3. Modify script.js
# First, clean v9902_life grade 6
# Wait, let's just do it cleanly by extracting grades_9902_full.json, slicing G6, and formatting it
data_9902 = json.load(codecs.open('c:/Users/SB/Desktop/연습용/grades_9902_full.json', 'r', 'utf-8'))
data_9902[5]['items'] = data_9902[5]['items'][:14]

def replace_block(text, version, block_name, new_val_str):
    v_start = text.find(f'"{version}": {{')
    if v_start == -1: v_start = text.find(f'{version}: {{')
    b_start = text.find(f'{block_name}: [', v_start)
    
    # find end of this array
    brace_count = 0
    in_arr = False
    b_end = -1
    for i in range(b_start, len(text)):
        if text[i] == '[':
            brace_count += 1
            in_arr = True
        elif text[i] == ']':
            brace_count -= 1
            if in_arr and brace_count == 0:
                b_end = i
                break
    
    if b_end != -1:
        return text[:b_start] + f"{block_name}: {new_val_str}" + text[b_end+1:]
    return text

# Apply 99.02 fixes
script_text = replace_block(script_text, "v9902_life", "grades", json.dumps(data_9902, ensure_ascii=False, indent=8))

# Apply 95.02 fixes
script_text = replace_block(script_text, "v9502_life_9901", "grades", json.dumps(grades_9502, ensure_ascii=False, indent=8))
script_text = replace_block(script_text, "v9502_life_9901", "parts", parts_json_str)
script_text = replace_block(script_text, "v9502_life_9901", "explanations", json.dumps(explanations_9502, ensure_ascii=False, indent=8))

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated script.js successfully!")
