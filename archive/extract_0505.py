import re
import json
import codecs

def parse_docx_txt(filepath):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    chongchik = []
    adls = []
    parts = []
    
    current_section = None
    current_part = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if '① 총칙' in line:
            current_section = 'chongchik'
            i += 1
            continue
        elif '② 장해분류별 판정기준' in line:
            current_section = 'parts'
            i += 1
            continue
        elif '<붙 임>' in line or ('일상생활 기본동작(ADLs)' in line and '③' in line) or current_section == 'adls':
            if '<붙 임>' in line or '일상생활 기본동작(ADLs)' in line:
                current_section = 'adls'
                if '<붙 임>' in line or '일상생활 기본동작' in line:
                    adls.append(line)
                i += 1
                continue
            
        if current_section == 'chongchik':
            chongchik.append(line)
            i += 1
        elif current_section == 'adls':
            adls.append(line)
            i += 1
        elif current_section == 'parts':
            m = re.match(r'^(\d+)\.\s+(.*장해.*|.*추상.*)$', line)
            if m and len(line) < 30 and m.group(1).isdigit():
                if current_part:
                    parts.append(current_part)
                current_part = {
                    "category": line,
                    "items": [],
                    "explanations": []
                }
                i += 1
                
                while i < len(lines) and not re.match(r'^(\d+)\.\s+(.*장해.*|.*추상.*)$', lines[i]) and '<붙 임>' not in lines[i]:
                    if lines[i] == '가. 장해의 분류' or lines[i] == '장해의 분류' or lines[i] == '지급률':
                        i += 1
                        continue
                        
                    # More robust match for explanation start
                    if re.match(r'^나\.\s*장해', lines[i]):
                        i += 1
                        while i < len(lines) and not re.match(r'^(\d+)\.\s+(.*장해.*|.*추상.*)$', lines[i]) and '<붙 임>' not in lines[i]:
                            current_part["explanations"].append(lines[i])
                            i += 1
                        break
                    
                    items = []
                    rates = []
                    while i < len(lines) and not re.match(r'^나\.\s*장해', lines[i]) and '<붙 임>' not in lines[i]:
                        if re.match(r'^\d+\)', lines[i]):
                            items.append(lines[i])
                        elif re.match(r'^(\d+|10~100)$', lines[i]):
                            rates.append(lines[i])
                        i += 1
                        
                    for j in range(len(items)):
                        rate = rates[j] + "%" if j < len(rates) else "-"
                        if rate == "10~100%": rate = "10~100%"
                        desc = items[j]
                        current_part["items"].append({
                            "desc": desc,
                            "rate": rate
                        })
                    
                    if i < len(lines) and re.match(r'^나\.\s*장해', lines[i]):
                        continue
            else:
                i += 1
        else:
            i += 1

    if current_part:
        parts.append(current_part)

    explanations = []
    
    chongchik_html = "<br>".join(chongchik)
    chongchik_html = chongchik_html.replace('1. 장해의 정의', '<strong>1. 장해의 정의</strong>')
    chongchik_html = chongchik_html.replace('2. 신체부위', '<br><strong>2. 신체부위</strong>')
    chongchik_html = chongchik_html.replace('3. 기타', '<br><strong>3. 기타</strong>')
    
    explanations.append({
        "title": "① 총칙",
        "content": chongchik_html
    })
    
    for idx, p in enumerate(parts):
        exp_html = "<br>".join(p["explanations"])
        exp_html = re.sub(r'(다\.\s+.*?)(?=<br>|$)', r'<br><strong>\1</strong>', exp_html)
        exp_html = re.sub(r'(라\.\s+.*?)(?=<br>|$)', r'<br><strong>\1</strong>', exp_html)
        exp_html = re.sub(r'(마\.\s+.*?)(?=<br>|$)', r'<br><strong>\1</strong>', exp_html)
        
        # fix the weird bolding from line breaks
        exp_html = exp_html.replace('된<br><strong>다.', '된다.<br>')
        exp_html = exp_html.replace('한<br><strong>다.', '한다.<br>')
        exp_html = exp_html.replace('있<br><strong>다.', '있다.<br>')
        
        explanations.append({
            "title": p["category"],
            "content": exp_html
        })
        p["expIndices"] = [idx + 1]
        del p["explanations"]
        
    adls_html = "<br>".join(adls)
    adls_html = adls_html.replace('유형<br>제한 정도에 따른 지급률', '')
    explanations.append({
        "title": "③ <붙 임> 일상생활 기본동작(ADLs) 제한 장해평가표",
        "content": adls_html
    })
    
    final_data = {
        "type": "parts_and_exp",
        "grades": [],
        "parts": parts,
        "explanations": explanations
    }
    
    with codecs.open('c:/Users/SB/Desktop/연습용/v0505_data.json', 'w', 'utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print("Parsing done! Check v0505_data.json")

parse_docx_txt('c:/Users/SB/Desktop/연습용/parsed_0505.txt')
