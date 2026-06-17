import zipfile
import xml.etree.ElementTree as ET
import base64
import os
import re
import json
import codecs

def parse_docx_with_media(docx_path, out_json_path):
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
        'v': 'urn:schemas-microsoft-com:vml'
    }

    images_b64 = {}
    rels_map = {}

    try:
        with zipfile.ZipFile(docx_path) as z:
            # 1. Map relationships
            try:
                rels_xml = z.read('word/_rels/document.xml.rels')
                rels_root = ET.fromstring(rels_xml)
                rel_ns = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                for rel in rels_root.findall('.//rel:Relationship', rel_ns):
                    r_id = rel.get('Id')
                    target = rel.get('Target')
                    rels_map[r_id] = target
            except Exception as e:
                print(f"Error reading rels: {e}")

            # 2. Extract media to base64
            for item in z.namelist():
                if item.startswith('word/media/'):
                    ext = item.split('.')[-1].lower()
                    mime = 'image/jpeg'
                    if ext == 'png': mime = 'image/png'
                    elif ext == 'gif': mime = 'image/gif'
                    elif ext == 'emf': mime = 'image/x-emf'
                    elif ext == 'wmf': mime = 'image/x-wmf'
                    
                    data = z.read(item)
                    b64 = base64.b64encode(data).decode('utf-8')
                    # We store by target path relative to word/ e.g. media/image1.png
                    target_path = item.replace('word/', '')
                    images_b64[target_path] = f"data:{mime};base64,{b64}"

            # 3. Read document.xml
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            body = root.find('w:body', ns)
            
            blocks = []
            
            for elem in body:
                if elem.tag == f"{{{ns['w']}}}p":
                    # Parse paragraph
                    p_text = ""
                    for child in elem.iter():
                        if child.tag == f"{{{ns['w']}}}t" and child.text:
                            p_text += child.text
                        elif child.tag == f"{{{ns['a']}}}blip":
                            embed_id = child.get(f"{{{ns['r']}}}embed")
                            if embed_id and embed_id in rels_map:
                                target = rels_map[embed_id]
                                if target in images_b64:
                                    img_tag = f'<img src="{images_b64[target]}" class="doc-image" style="max-width:100%; display:block; margin:10px auto;">'
                                    p_text += img_tag
                        elif child.tag == f"{{{ns['v']}}}imagedata":
                            embed_id = child.get(f"{{{ns['r']}}}id")
                            if embed_id and embed_id in rels_map:
                                target = rels_map[embed_id]
                                if target in images_b64:
                                    img_tag = f'<img src="{images_b64[target]}" class="doc-image" style="max-width:100%; display:block; margin:10px auto;">'
                                    p_text += img_tag
                    
                    p_text = p_text.strip()
                    if p_text:
                        blocks.append(p_text)
                        
                elif elem.tag == f"{{{ns['w']}}}tbl":
                    # Parse table
                    table_html = ['<table class="doc-table" style="width:100%; border-collapse: collapse; margin-top:10px; margin-bottom:10px; font-size:14px; border:1px solid #ccc;">']
                    for row in elem.findall('.//w:tr', ns):
                        table_html.append('<tr>')
                        for cell in row.findall('.//w:tc', ns):
                            cell_paragraphs = []
                            for p in cell.findall('.//w:p', ns):
                                p_text = ""
                                for t in p.findall('.//w:t', ns):
                                    if t.text:
                                        p_text += t.text
                                p_text = p_text.strip()
                                if p_text:
                                    cell_paragraphs.append(p_text)
                            cell_content = "<br>".join(cell_paragraphs)
                            table_html.append(f'<td style="border: 1px solid #ccc; padding: 8px;">{cell_content}</td>')
                        table_html.append('</tr>')
                    table_html.append('</table>')
                    blocks.append("".join(table_html))

    except Exception as e:
        print(f"Failed to process docx: {e}")
        return

    # Now we have blocks containing text, images, and tables.
    chongchik = []
    adls = []
    parts = []
    
    current_section = None
    current_part = None
    
    i = 0
    while i < len(blocks):
        line = blocks[i]
        
        # Check if it's a structural plain text header (not table)
        if not line.startswith('<table') and not line.startswith('<img'):
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
            if not line.startswith('<table') and not line.startswith('<img'):
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
                    
                    while i < len(blocks) and not (not blocks[i].startswith('<table') and not blocks[i].startswith('<img') and re.match(r'^(\d+)\.\s+(.*장해.*|.*추상.*)$', blocks[i])) and '<부표>' not in blocks[i] and blocks[i] != '일상생활 기본동작(ADLs) 제한 장해평가표':
                        if blocks[i] in ['가. 장해의 분류', '장해의 분류', '지급률']:
                            i += 1
                            continue
                            
                        # If we see a table right before "나. 장해판정기준", it's the rates table!
                        if blocks[i].startswith('<table') and not current_part["explanations"]:
                            # Parse the HTML table back into items and rates
                            tds = re.findall(r'<td.*?>(.*?)</td>', blocks[i])
                            if len(tds) >= 2:
                                if len(tds) == 4: # header row (2) + data row (2)
                                    desc_list = tds[2].split('<br>')
                                    rate_list = tds[3].split('<br>')
                                    for j in range(len(desc_list)):
                                        r = rate_list[j] + "%" if j < len(rate_list) else "-"
                                        if r == "10~100%": r = "10~100%"
                                        current_part["items"].append({
                                            "desc": desc_list[j].strip(),
                                            "rate": r.strip()
                                        })
                                else:
                                    # Fallback: each row is an item
                                    for row_idx in range(2, len(tds), 2):
                                        if row_idx + 1 < len(tds):
                                            d = tds[row_idx].strip()
                                            r = tds[row_idx+1].strip() + "%"
                                            if r == "10~100%": r = "10~100%"
                                            current_part["items"].append({
                                                "desc": d,
                                                "rate": r
                                            })
                            i += 1
                            continue
                            
                        # Explanation start
                        if not blocks[i].startswith('<table') and not blocks[i].startswith('<img') and re.match(r'^나\.\s*장해', blocks[i]):
                            i += 1
                            while i < len(blocks) and not (not blocks[i].startswith('<table') and not blocks[i].startswith('<img') and re.match(r'^(\d+)\.\s+(.*장해.*|.*추상.*)$', blocks[i])) and '<부표>' not in blocks[i] and blocks[i] != '일상생활 기본동작(ADLs) 제한 장해평가표':
                                current_part["explanations"].append(blocks[i])
                                i += 1
                            break
                        
                        i += 1
                else:
                    i += 1
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
    
    with codecs.open(out_json_path, 'w', 'utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print(f"Parsing done! Found {len(parts)} parts.")
    print(f"Items in part 1: {len(parts[0]['items']) if parts else 0}")
    print(f"Items in part 13: {len(parts[-1]['items']) if parts else 0}")

parse_docx_with_media('c:/Users/SB/Desktop/연습용/장해분류표_최신.docx', 'c:/Users/SB/Desktop/연습용/latest_data_media.json')
