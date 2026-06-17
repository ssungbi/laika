import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
v9902_start = text.find('"v9902_life": {')
v9902_text = text[v9902_start:text.find('};', v9902_start)]

grades_start = v9902_text.find('grades: [')
grades_end = v9902_text.find('parts: [', grades_start)
grades_text = v9902_text[grades_start:grades_end]

mapping = {}
grade_items = re.findall(r'category:\s*"(제\d+급)".*?items:\s*\[(.*?)\]', grades_text, re.DOTALL)
for grade_cat, items_text in grade_items:
    g_match = re.search(r'\d+', grade_cat)
    g_num = g_match.group(0)
    
    items = re.findall(r'\{\s*desc:\s*"([^"]+)",', items_text)
    for idx, desc in enumerate(items):
        m_num = idx + 1
        clean_desc = re.sub(r'^\d+\.\s*', '', desc).strip()
        clean_desc = re.sub(r'<[^>]+>', '', clean_desc).strip()
        mapping[clean_desc] = f"{g_num}급{m_num}항"

parts_start = v9902_text.find('parts: [')
exp_start = v9902_text.find('explanations: [', parts_start)
parts_text = v9902_text[parts_start:exp_start]

part_items = re.findall(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', parts_text)

print("Original Parts Text matches mapping?")
for desc, rate in part_items[:10]:
    clean_desc = re.sub(r'^\d+\.\s*', '', desc).strip()
    clean_desc = re.sub(r'<[^>]+>', '', clean_desc).strip()
    
    # Check exact match first
    if clean_desc in mapping:
        print(f"EXACT: '{clean_desc}' -> {mapping[clean_desc]}")
    else:
        print(f"NO EXACT MATCH: '{clean_desc}'")
        # Let's see what the closest match in mapping is using SequenceMatcher
        from difflib import SequenceMatcher
        best_match = ""
        best_score = 0
        for k in mapping.keys():
            score = SequenceMatcher(None, k, clean_desc).ratio()
            if score > best_score:
                best_score = score
                best_match = k
        print(f"  -> BEST FUZZY: '{best_match}' -> {mapping.get(best_match)} (Score: {best_score})")

