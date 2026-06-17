import codecs
import re
import json

html = codecs.open('c:/Users/SB/Desktop/연습용/sago25_utf8.html', 'r', 'utf-8').read()

# 1. We ONLY care about the table. Let's find the table or just strip all tags EXCEPT <br>
# Remove everything before the first "제1급"
start_idx = html.find('>제1급<')
html = html[start_idx:]

# Remove <script> tags just in case
html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.I|re.DOTALL)

# Replace <br> and <p> with a space, NOT a newline! Because we want sentences to be contiguous!
# Wait! If there are separate paragraphs that don't belong to the sentence? 
# Actually, the items are just numbered. If we just replace ALL tags with a space, we can then regex extract by number!
text = re.sub(r'<[^>]+>', ' ', html)
# Clean up whitespace
text = re.sub(r'\s+', ' ', text).strip()

# Now text is one giant string: "제1급 1. 두눈의 시력을 완전 영구히 잃었을 때 2. 말 또는 ... 제2급 1. ..."
# Let's split by "제X급"
grades_data = re.split(r'(제[1-6]급)', text)

grades = []
# grades_data[0] is empty or garbage
for i in range(1, len(grades_data), 2):
    grade_name = grades_data[i]
    grade_text = grades_data[i+1]
    
    # extract items
    items = []
    # match "1. 블라블라 2. 블라블라"
    # We can split by "\s+(\d+)\.\s+"
    # But wait, the first item might just be " 1. "
    # Let's find all occurrences of " \d+. " or "^\d+. "
    matches = list(re.finditer(r'(?:^|\s)(\d+)\.\s+', grade_text))
    
    for j in range(len(matches)):
        start = matches[j].end()
        end = matches[j+1].start() if j+1 < len(matches) else len(grade_text)
        
        item_text = grade_text[start:end].strip()
        items.append({"desc": f"{matches[j].group(1)}. {item_text}", "rate": grade_name[-2:]})
        
    grades.append({"category": grade_name, "items": items})

# Let's verify lengths
for g in grades:
    print(f"{g['category']}: {len(g['items'])} items")

# Check if item texts are complete
print(json.dumps(grades[3], ensure_ascii=False, indent=2))

codecs.open('c:/Users/SB/Desktop/연습용/grades_9902_full.json', 'w', 'utf-8').write(json.dumps(grades, ensure_ascii=False, indent=4))
