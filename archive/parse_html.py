import codecs
import re
import json

html = codecs.open('c:/Users/SB/Desktop/연습용/sago25_utf8.html', 'r', 'utf-8').read()

# 1. Convert <br> and <p> and <tr> and <td> to newlines to separate blocks
html = re.sub(r'<(br|p|tr|td)[^>]*>', '\n', html, flags=re.I)
html = re.sub(r'</(p|tr|td)>', '\n', html, flags=re.I)

# 2. Remove all other HTML tags (like <a>, <span>, <font>, <b>, etc.)
html = re.sub(r'<[^>]+>', '', html)

# 3. Clean up multiple newlines
text = re.sub(r'\n\s*\n+', '\n', html).strip()

# Now extract grades
grades = []
current_grade = None
current_grade_num = ""

for line in text.split('\n'):
    line = line.strip()
    if not line: continue
    
    m_grade = re.match(r'^제([1-6])급', line)
    if m_grade:
        current_grade_num = m_grade.group(1)
        current_grade = "제" + current_grade_num + "급"
        grades.append({"category": current_grade, "items": []})
        continue
        
    if current_grade and re.match(r'^\d+\.', line):
        # clean line
        line = re.sub(r'\s+', ' ', line)
        grades[-1]["items"].append({"desc": line, "rate": current_grade_num + "급"})

# Now let's see how many items per grade
for g in grades:
    print(f"{g['category']}: {len(g['items'])} items")

# Let's write the exact grades to a JSON file
codecs.open('c:/Users/SB/Desktop/연습용/grades_9902_full.json', 'w', 'utf-8').write(json.dumps(grades, ensure_ascii=False, indent=4))
