import codecs
import json
import re

# Load 9502 grades
script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx1 = script.find('v9502_life_9901')
g_start = script.find('grades: [', idx1)
g_end = script.find('parts: [', g_start)
grades_text = script[g_start+8:g_end].strip()
if grades_text.endswith(','): grades_text = grades_text[:-1]
grades_9502 = json.loads(grades_text)

# Build a dictionary of clean desc -> rate for exact matching
map_9502 = {}
for g in grades_9502:
    for item in g['items']:
        clean = re.sub(r'^\d+\.\s*', '', item['desc']).strip()
        clean = re.sub(r'<[^>]+>', '', clean).strip()
        rate = f"{g['category'][-2:]}{item['desc'].split('.')[0]}항"
        map_9502[clean] = rate
        # also add without spaces for super exact match
        map_9502[clean.replace(' ', '')] = rate

# Now load 9902 parts to see what we have
v9902_idx = script.find('"v9902_life": {')
p_start = script.find('parts: [', v9902_idx)
p_end = script.find('explanations: [', p_start)
parts_text = script[p_start+7:p_end].strip()
if parts_text.endswith(','): parts_text = parts_text[:-1]
parts_9902 = json.loads(parts_text)

for cat in parts_9902:
    print(f"\n[{cat['category']}]")
    for item in cat['items']:
        clean = re.sub(r'^\d+\.\s*', '', item['desc']).strip()
        clean = re.sub(r'<[^>]+>', '', clean).strip()
        clean_ns = clean.replace(' ', '')
        
        if clean in map_9502:
            print(f"  EXACT MATCH: {item['desc']} -> {map_9502[clean]}")
        elif clean_ns in map_9502:
            print(f"  NO-SPACE MATCH: {item['desc']} -> {map_9502[clean_ns]}")
        else:
            print(f"  MISSING (will delete): {item['desc']}")
