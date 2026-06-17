import codecs
import json
import re

html = codecs.open('c:/Users/SB/Desktop/연습용/user_9807_data.html', 'r', 'utf-8').read()
parts_html, exp_html = html.split('---')

# 1. Parse Parts
parts = []
tbody = re.search(r'<tbody>(.*?)</tbody>', parts_html, re.DOTALL).group(1)
trs = re.findall(r'<tr>(.*?)</tr>', tbody, re.DOTALL)

for i, tr in enumerate(trs):
    cat_match = re.search(r'<strong>(.*?)</strong>', tr)
    if not cat_match: continue
    cat_name = cat_match.group(1).strip()
    
    td = re.search(r'<td>(.*?)</td>', tr, re.DOTALL).group(1)
    items_matches = re.findall(r'<li><span>(\d+\))</span>(.*?)</li>', td)
    
    th = re.search(r'<th>(.*?)</th>', tr, re.DOTALL).group(1)
    rate_lis = re.findall(r'<li>(.*?)</li>', th)
    rates = [r.strip() for r in rate_lis if r.strip() not in ('', '　')]
    
    cat_items = []
    for j, (num, desc) in enumerate(items_matches):
        rate_val = rates[j] + "%" if j < len(rates) else "-"
        desc = re.sub(r'<[^>]+>', '', desc).strip()
        cat_items.append({"desc": f"{num}) {desc}", "rate": rate_val})
        
    parts.append({
        "category": f"{i+1}. {cat_name}",
        "items": cat_items,
        "expIndices": []
    })

# 2. Parse Explanations
explanations = []
# The first few <li> outside of <ol> are general notes
general_notes = re.findall(r'<li>(.*?)</li>', exp_html.split('<p>&lt;용어풀이&gt;</p>')[0], re.DOTALL)
for i, note in enumerate(general_notes):
    clean_note = re.sub(r'<[^>]+>', '', note).strip()
    if clean_note:
        explanations.append({
            "title": f"일반사항 {i+1}",
            "content": clean_note
        })

# 용어풀이
terms_html = exp_html.split('<p>&lt;용어풀이&gt;</p>')[1]
term_lis = re.findall(r'<li>([^<]+)(.*?)</li>', terms_html, re.DOTALL)

# Because there are nested ol/li, we need a better parser.
# Let's split by <li> that starts with a number.
terms = re.split(r'<li>(?=\d+\.)', terms_html)
for term in terms:
    term = term.strip()
    if not term: continue
    m = re.match(r'(\d+)\.\s*([^\n<]+)(.*)', term, re.DOTALL)
    if not m:
        m = re.match(r'(\d+)\s*([^\n<]+)(.*)', term, re.DOTALL)
        
    if m:
        title_num = m.group(1).strip()
        title_text = m.group(2).strip()
        content_html = m.group(3).strip()
        # strip out remaining tags except <p> which we turn into newlines
        content = re.sub(r'<p>', '', content_html)
        content = re.sub(r'</p>', '\\n', content)
        content = re.sub(r'<li>', '', content)
        content = re.sub(r'</li>', '\\n', content)
        content = re.sub(r'<[^>]+>', '', content).strip()
        # Clean up multiple newlines
        content = re.sub(r'\\n\s*\\n', '\\n', content)
        
        explanations.append({
            "title": f"{title_num}. {title_text}",
            "content": content.strip()
        })

# Mapping Parts to Explanations based on title matches
# This is tricky because the titles are like "1. 귓바퀴의 대부분의 결손", "2. 이의 결손", etc.
exp_mapping = {
    "1. 눈의 장애": [],
    "2. 귀(耳)의 장애": [4], # 귓바퀴 (index 4) - Note: index depends on general notes length
    "3. 코(鼻)의 장애": [],
    "4. 씹거나 말하는 기능의 장애": [5], # 이의 결손
    "5. 외모(얼굴, 머리, 목)의 추상장해": [6, 7], # 외모의 뚜렷한 추상, 외모의 추상
    "6. 등뼈의 장애": [8], # 등뼈의 장해
    "7. 팔 또는 다리의 장애": [9], # 팔, 다리의 1관절기능 장해
    "8. 손가락의 장애": [10, 11], # 손/발가락뼈 일부 잃음, 뚜렷한 장해
    "9. 발(가락)의 장애": [10, 11], # 손/발가락뼈 일부 잃음, 뚜렷한 장해
    "10. 흉ㆍ복부장기의 장애": [12], # 흉복부장기의 장해
    "11. 정신ㆍ신경계통의 장애": [13] # 사지 완전마비 등
}

# The explanations array starts with 4 general notes. So index 4 is the 1st term.
parts_json = parts
for p in parts_json:
    cat = p["category"]
    if cat in exp_mapping:
        p["expIndices"] = exp_mapping[cat]

parts_json_str = json.dumps(parts_json, ensure_ascii=False, indent=12)
parts_json_str = parts_json_str.replace('\n            {', ' {').replace('\n            }', ' }')
exp_str = json.dumps(explanations, ensure_ascii=False, indent=8)

new_v9807 = f'''"v9807_nonlife": {{
        type: "parts_and_exp",
        grades: [],
        parts: {parts_json_str},
        explanations: {exp_str}
    }},'''

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

dummy_line = '"v9807_nonlife": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],'
if dummy_line in script_text:
    script_text = script_text.replace(dummy_line, new_v9807)
else:
    print("Could not find dummy line to replace!")

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated v9807_nonlife!")
