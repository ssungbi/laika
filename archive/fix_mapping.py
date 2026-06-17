import codecs
import re
import json

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# find v9902_life
start_idx = script.find('"v9902_life": {')
# wait, it's just 'v9902_life: {' in the original?
if start_idx == -1:
    start_idx = script.find('v9902_life: {')
    
end_idx = script.find('explanations: [', start_idx)

v9902_text = script[start_idx:end_idx]

# 1. extract grades
grades_start = v9902_text.find('grades: [')
grades_end = v9902_text.find('parts: [', grades_start)
grades_text = v9902_text[grades_start:grades_end]

mapping = {}

current_grade = ""
# Match { desc: "...", rate: "1급" } inside grades
grade_items = re.findall(r'category:\s*"(제\d+급)".*?items:\s*\[(.*?)\]', grades_text, re.DOTALL)
for grade_cat, items_text in grade_items:
    g_match = re.search(r'\d+', grade_cat)
    g_num = g_match.group(0)
    
    # parse items
    items = re.findall(r'\{\s*desc:\s*"([^"]+)",', items_text)
    for idx, desc in enumerate(items):
        m_num = idx + 1
        # clean desc for matching (remove leading numbers like "1. ")
        clean_desc = re.sub(r'^\d+\.\s*', '', desc).strip()
        mapping[clean_desc] = f"{g_num}급{m_num}항"

# 2. apply to parts
parts_start = v9902_text.find('parts: [')
parts_text = v9902_text[parts_start:]

def replace_part(match):
    desc = match.group(1)
    rate = match.group(2)
    clean_desc = re.sub(r'^\d+\.\s*', '', desc).strip()
    # also remove tooltips if they are embedded
    clean_desc = re.sub(r'<[^>]+>', '', clean_desc).strip()
    
    # fuzzy match if exact fails
    best_match = ""
    best_score = 0
    for k, v in mapping.items():
        # simple character intersection
        score = sum(1 for c in k if c in clean_desc) / len(k)
        if score > best_score:
            best_score = score
            best_match = k
            
    if best_score > 0.9:
        return f'{{ desc: "{desc}", rate: "{mapping[best_match]}" }}'
    return match.group(0)

new_parts_text = re.sub(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', replace_part, parts_text)

new_script = script[:start_idx + parts_start] + new_parts_text + script[end_idx:]

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(new_script)
print("Updated parts with correct N급M항!")
