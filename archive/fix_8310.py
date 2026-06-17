import codecs
import json
import re

user_data = codecs.open('c:/Users/SB/Desktop/연습용/user_data_8310.txt', 'r', 'utf-8').read()

exp_start = user_data.find('장해등급분류 해설')
grades_text = user_data[:exp_start].strip()
exp_text = user_data[exp_start:].strip()

grades_8310 = []
current_grade = None

for line in grades_text.split('\n'):
    line = line.strip()
    if not line: continue
    
    m = re.match(r'^([1-6])급\s+(.*)', line)
    if m:
        current_grade = f"제{m.group(1)}급"
        grades_8310.append({"category": current_grade, "items": []})
        desc = m.group(2).strip()
        if desc and re.match(r'^\d+\.', desc):
            grades_8310[-1]['items'].append({"desc": desc, "rate": f"{m.group(1)}급"})
    elif current_grade and re.match(r'^\d+\.', line):
        grades_8310[-1]['items'].append({"desc": line, "rate": current_grade[-2:]})

explanations_8310 = []
exp_blocks = re.split(r'\n(?=\d+\.\s+")', exp_text)
for block in exp_blocks:
    block = block.strip()
    if not block: continue
    m = re.match(r'\d+\.\s+"([^"]+)"\n(.*)', block, re.DOTALL)
    if m:
        explanations_8310.append({
            "title": m.group(1),
            "content": m.group(2).strip()
        })
    elif "장해등급분류 해설" not in block:
        lines = block.split('\n', 1)
        if len(lines) > 1:
            explanations_8310.append({
                "title": lines[0].strip(),
                "content": lines[1].strip()
            })

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

for g in grades_8310:
    rate = g['category'][-2:]
    for item in g['items']:
        desc = item['desc']
        clean = re.sub(r'^\d+\.\s*', '', desc)
        full_rate = f"{rate}{desc.split('.')[0]}항"
        
        if '눈의' in desc or '시력' in desc:
            cat_map["눈의 장해"].append({"desc": desc, "rate": full_rate})
        elif '귀의' in desc or '청력' in desc:
            cat_map["귀의 장해"].append({"desc": desc, "rate": full_rate})
        elif '코가' in desc:
            cat_map["코의 장해"].append({"desc": desc, "rate": full_rate})
        elif '말 또는' in desc or '씹어먹는' in desc:
            cat_map["입의 장해"].append({"desc": desc, "rate": full_rate})
        elif '척추' in desc:
            cat_map["척추의 장해"].append({"desc": desc, "rate": full_rate})
        elif '손가락' in desc:
            cat_map["손가락의 장해"].append({"desc": desc, "rate": full_rate})
        elif '발가락' in desc:
            cat_map["발가락의 장해"].append({"desc": desc, "rate": full_rate})
        elif '팔' in desc or '다리' in desc or '관절' in desc:
            cat_map["팔, 다리의 장해"].append({"desc": desc, "rate": full_rate})
        elif '흉복부' in desc or '비장' in desc or '신장' in desc or '장기' in desc:
            cat_map["흉복부 장기 및 비뇨생식기 장해"].append({"desc": desc, "rate": full_rate})
        elif '중추신경계' in desc or '정신에' in desc:
            cat_map["신경계 정신행동 장해"].append({"desc": desc, "rate": full_rate})
        else:
            print("UNCATEGORIZED:", desc)

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
    "1. 눈의 장해": [2, 3],
    "2. 귀의 장해": [6, 7],
    "3. 코의 장해": [8],
    "4. 입의 장해": [4, 5],
    "5. 척추의 장해": [11],
    "6. 팔, 다리의 장해": [9, 10, 14],
    "7. 손가락의 장해": [12, 14],
    "8. 발가락의 장해": [13, 14],
    "9. 흉복부 장기 및 비뇨생식기 장해": [],
    "10. 신경계 정신행동 장해": [0, 1]
}

parts_8310 = []
for cat_name in cat_names:
    base_name = cat_name.split('. ')[1]
    items = cat_map[base_name]
    if items:
        parts_8310.append({
            "category": cat_name,
            "items": items,
            "expIndices": exp_mapping[cat_name]
        })

parts_json_str = json.dumps(parts_8310, ensure_ascii=False, indent=12)
parts_json_str = parts_json_str.replace('\n            {', ' {').replace('\n            }', ' }')
grades_str = json.dumps(grades_8310, ensure_ascii=False, indent=8)
exp_str = json.dumps(explanations_8310, ensure_ascii=False, indent=8)

new_v8310 = f'''"v8310_life": {{
        type: "tab",
        grades: {grades_str},
        parts: {parts_json_str},
        explanations: {exp_str}
    }},'''

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# Replace the specific dummy line
dummy_line = '"v8310_life": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],'
script_text = script_text.replace(dummy_line, new_v8310)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated script.js for 8310 correctly!")
