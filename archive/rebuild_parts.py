import codecs
import json
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx1 = script.find('v9502_life_9901')
g_start = script.find('grades: [', idx1)
g_end = script.find('parts: [', g_start)
grades_text = script[g_start+8:g_end].strip()
if grades_text.endswith(','): grades_text = grades_text[:-1]
grades_9502 = json.loads(grades_text)

# Categories
cat_map = {
    "눈의 장해": [],
    "귀의 장해": [],
    "코의 장해": [],
    "입의 장해": [],
    "척추의 장해": [],
    "팔, 다리의 장해": [],
    "손가락의 장해": [],
    "발가락의 장해": [],
    "흉복부 장기 및 비뇨생식기 장해": [],
    "신경계 정신행동 장해": []
}

for g in grades_9502:
    rate = g['category'][-2:]
    for item in g['items']:
        desc = item['desc']
        clean = re.sub(r'^\d+\.\s*', '', desc)
        
        full_rate = f"{rate}{desc.split('.')[0]}항"
        
        # Categorize
        if '눈의' in desc or '시력' in desc:
            cat_map["눈의 장해"].append({"desc": desc, "rate": full_rate})
        elif '귀의' in desc or '청력' in desc:
            cat_map["귀의 장해"].append({"desc": desc, "rate": full_rate})
        elif '코가' in desc:
            cat_map["코의 장해"].append({"desc": desc, "rate": full_rate})
        elif '말 또는' in desc:
            cat_map["입의 장해"].append({"desc": desc, "rate": full_rate})
        elif '척추' in desc:
            cat_map["척추의 장해"].append({"desc": desc, "rate": full_rate})
        elif '손가락' in desc:
            cat_map["손가락의 장해"].append({"desc": desc, "rate": full_rate})
        elif '발가락' in desc:
            cat_map["발가락의 장해"].append({"desc": desc, "rate": full_rate})
        elif '팔' in desc or '다리' in desc or '관절' in desc:
            cat_map["팔, 다리의 장해"].append({"desc": desc, "rate": full_rate})
        elif '흉복부' in desc or '비장' in desc or '신장' in desc:
            cat_map["흉복부 장기 및 비뇨생식기 장해"].append({"desc": desc, "rate": full_rate})
        elif '중추신경계' in desc or '정신에' in desc:
            cat_map["신경계 정신행동 장해"].append({"desc": desc, "rate": full_rate})
        else:
            print("UNCATEGORIZED:", desc)

# Build parts array
parts_9502 = []
cat_names = [
    "1. 눈의 장해",
    "2. 귀의 장해",
    "3. 코의 장해",
    "4. 입의 장해",
    "5. 척추의 장해",
    "6. 팔, 다리의 장해",
    "7. 손가락의 장해",
    "8. 발가락의 장해",
    "9. 흉복부 장기 및 비뇨생식기 장해",
    "10. 신경계 정신행동 장해"
]

exp_mapping = {
    "1. 눈의 장해": [4, 5],
    "2. 귀의 장해": [8, 9],
    "3. 코의 장해": [10],
    "4. 입의 장해": [6, 7],
    "5. 척추의 장해": [13],
    "6. 팔, 다리의 장해": [11, 12, 16],
    "7. 손가락의 장해": [14, 16],
    "8. 발가락의 장해": [15, 16],
    "9. 흉복부 장기 및 비뇨생식기 장해": [],
    "10. 신경계 정신행동 장해": [1, 2, 3]
}

# The user's explanations might have different numbers, but let's just keep the indices or map them.
# The user's text for explanations has numbers: 1 to 16.
# My script parse explanations and keeps the order. We should use the actual indices.
# Let's map it based on string matching.

for i, cat_name in enumerate(cat_names):
    base_name = cat_name.split('. ')[1]
    items = cat_map[base_name]
    if items:
        # Sort items by grade, then by item number? They are already mostly in order of grades.
        # But wait, the standard display is by grade then number. Since we iterated over grades, they are sorted!
        parts_9502.append({
            "category": cat_name,
            "items": items,
            "expIndices": exp_mapping[cat_name]
        })

parts_json_str = json.dumps(parts_9502, ensure_ascii=False, indent=12)
parts_json_str = parts_json_str.replace('\n            {', ' {').replace('\n            }', ' }')

# Replace in script
idx2 = script.find('parts: [', idx1)
idx3 = script.find('explanations: [', idx2)
script = script[:idx2] + "parts: " + parts_json_str + ",\n        " + script[idx3:]

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script)
print("Parts exactly rebuilt from grades_9502!")
