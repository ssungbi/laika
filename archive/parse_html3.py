import codecs
import re
import json

html = codecs.open('c:/Users/SB/Desktop/연습용/sago25_utf8.html', 'r', 'utf-8').read()

# find the table rows containing grades
grades = []

# The structure is <TD ...> <SPAN ...> <FONT ...>제1급</FONT></SPAN></P></TD> <TD> ... </TD>
# We can find all occurrences of "제1급", "제2급", etc inside FONT or TD
matches = list(re.finditer(r'>제([1-6])급<', html))

for i in range(len(matches)):
    start = matches[i].end()
    end = matches[i+1].start() if i+1 < len(matches) else html.find('</table>', start)
    if end == -1: end = len(html)
    
    grade_num = matches[i].group(1)
    grade_html = html[start:end]
    
    # Extract text from this block
    # replace <br>, <p> with space
    text = re.sub(r'<[^>]+>', ' ', grade_html)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # match items
    items = []
    item_matches = list(re.finditer(r'(?:^|\s)(\d+)\.\s+', text))
    for j in range(len(item_matches)):
        i_start = item_matches[j].end()
        i_end = item_matches[j+1].start() if j+1 < len(item_matches) else len(text)
        item_text = text[i_start:i_end].strip()
        items.append({"desc": f"{item_matches[j].group(1)}. {item_text}", "rate": f"{grade_num}급"})
        
    grades.append({"category": f"제{grade_num}급", "items": items})

for g in grades:
    print(f"{g['category']}: {len(g['items'])} items")

# Check if item texts are complete
print(json.dumps(grades[3], ensure_ascii=False, indent=2))

codecs.open('c:/Users/SB/Desktop/연습용/grades_9902_full.json', 'w', 'utf-8').write(json.dumps(grades, ensure_ascii=False, indent=4))
