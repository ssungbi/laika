import re
import json

text = open('c:/Users/SB/Desktop/연습용/sago25_clean.txt', encoding='utf-8').read()

# 1. Extract Grades
grades_text = text[text.find('1급'):text.find('장해해설 및 평가기준')]
grades = []
current_grade = None

for line in grades_text.split('\n'):
    line = line.strip()
    if not line: continue
    
    m_grade = re.match(r'제?([1-6])급', line)
    if m_grade:
        current_grade = "제" + m_grade.group(1) + "급"
        grades.append({"category": current_grade, "items": []})
        continue
        
    if current_grade and re.match(r'^\d+\.', line):
        grades[-1]["items"].append({"desc": line, "rate": current_grade[-2:]})

# 2. Extract Explanations
exp_text = text[text.find('장해해설 및 평가기준'):]
explanations = []
current_exp = None
content = []

for line in exp_text.split('\n'):
    line = line.strip()
    if not line: continue
    if '장해해설 및 평가기준' in line: continue
    
    m_exp = re.match(r'^(\d+)\.\s+(.*)', line)
    if m_exp:
        if current_exp:
            explanations.append({
                "id": f"exp{len(explanations)+1}",
                "title": current_exp,
                "content": "<br>".join(content)
            })
        current_exp = m_exp.group(0)
        content = []
    else:
        if current_exp:
            content.append(line)

if current_exp:
    explanations.append({
        "id": f"exp{len(explanations)+1}",
        "title": current_exp,
        "content": "<br>".join(content)
    })

out = {"grades": grades, "explanations": explanations}
open('c:/Users/SB/Desktop/연습용/parsed_9902.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=4))
