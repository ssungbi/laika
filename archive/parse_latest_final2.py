import codecs
import re
import json

def parse_docx_txt(filepath, outpath):
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
        elif '<부표>' in line or line == '일상생활 기본동작(ADLs) 제한 장해평가표':
            if current_section != 'adls':
                current_section = 'adls'
                if '<부표>' in line or '일상생활 기본동작' in line:
                    adls.append(line)
            else:
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
            # Match part header e.g. "1. 눈의 장해"
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
                
                while i < len(lines) and not re.match(r'^(\d+)\.\s+(.*장해.*|.*추상.*)$', lines[i]) and '<부표>' not in lines[i] and lines[i] != '일상생활 기본동작(ADLs) 제한 장해평가표':
                    if lines[i] in ['가. 장해의 분류', '장해의 분류', '지급률']:
                        i += 1
                        continue
                        
                    # Explanation start
                    if re.match(r'^나\.\s*장해', lines[i]):
                        i += 1
                        while i < len(lines) and not re.match(r'^(\d+)\.\s+(.*장해.*|.*추상.*)$', lines[i]) and '<부표>' not in lines[i] and lines[i] != '일상생활 기본동작(ADLs) 제한 장해평가표':
                            current_part["explanations"].append(lines[i])
                            i += 1
                        break
                    
                    # Parse items and rates
                    items = []
                    rates = []
                    while i < len(lines) and not re.match(r'^나\.\s*장해', lines[i]) and '<부표>' not in lines[i] and lines[i] != '일상생활 기본동작(ADLs) 제한 장해평가표':
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
    chongchik_html = chongchik_html.replace('3. 장해지급률', '<br><strong>3. 장해지급률 판정기준</strong>')
    
    explanations.append({
        "title": "① 총칙",
        "content": chongchik_html
    })
    
    for idx, p in enumerate(parts):
        exp_html = "<br>".join(p["explanations"])
        
        explanations.append({
            "title": p["category"],
            "content": exp_html
        })
        p["expIndices"] = [idx + 1]
        del p["explanations"]
        
    adls_html = "<br>".join(adls)
    explanations.append({
        "title": "③ <부표> 일상생활 기본동작(ADLs) 제한 장해평가표",
        "content": adls_html
    })
    
    final_data = {
        "type": "parts_and_exp",
        "grades": [],
        "parts": parts,
        "explanations": explanations
    }
    
    with codecs.open(outpath, 'w', 'utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print(f"Parsing done! Found {len(parts)} parts.")
    print(f"Items in part 1: {len(parts[0]['items']) if parts else 0}")
    print(f"Items in part 13: {len(parts[-1]['items']) if parts else 0}")

parse_docx_txt('c:/Users/SB/Desktop/연습용/parsed_latest.txt', 'c:/Users/SB/Desktop/연습용/latest_data.json')
