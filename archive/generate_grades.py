import re
import json

text = open('c:/Users/SB/Desktop/연습용/check_sago.txt', encoding='utf-8').read()

grades = []
current_grade = None

for line in text.split('\n'):
    line = line.strip()
    if not line: continue
    
    m_grade = re.match(r'제?([1-6])급', line)
    if m_grade:
        current_grade = "제" + m_grade.group(1) + "급"
        grades.append({"category": current_grade, "items": []})
        continue
        
    if current_grade and re.match(r'^\d+\.', line):
        grades[-1]["items"].append({"desc": line, "rate": current_grade[-2:]})

# Now print it
print(json.dumps(grades, ensure_ascii=False, indent=4))
