import urllib.request, ssl
import re
import json
import time
import os
import random
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_url(url):
    req = urllib.request.Request(url, headers=headers)
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, context=ctx) as res:
                content_bytes = res.read()
                try:
                    return content_bytes.decode('utf-8')
                except:
                    return content_bytes.decode('euc-kr', errors='replace')
        except Exception as e:
            time.sleep(1)
    return ""


def parse_tree_from_html(html, chart_type):
    nodes = {}
    root_nodes = []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    depth1_ul = soup.find('ul', class_='depth')
    if depth1_ul:
        for li in depth1_ul.find_all('li', recursive=False):
            a_tag = li.find('a', onclick=re.compile(r"hashchange\('([^']+)'\)"))
            if a_tag:
                node_id = re.search(r"hashchange\('([^']+)'\)", a_tag['onclick']).group(1)
                text = a_tag.find('span', class_='txt').get_text(strip=True)
                node = {'id': node_id, 'text': text, 'children': [], 'type': 'category'}
                nodes[node_id] = node
                root_nodes.append(node)

    script_content = soup.find_all('script')
    js_text = ""
    for sc in script_content:
        if sc.string and 'hashchange' in sc.string:
            js_text += sc.string

    cat_pattern = re.compile(r'_([A-Z0-9]+)_li\.innerHTML\s*=\s*[\'"](.*?)[\'"];')
    for match in cat_pattern.finditer(js_text):
        node_id = match.group(1)
        inner_html = match.group(2)
        
        cat_search = re.search(r'hashchange\(\\\'([A-Z0-9]+)\\\'\).*?<span[^>]*>(.*?)</span>', inner_html)
        if cat_search:
            text = cat_search.group(2)
            if node_id not in nodes:
                nodes[node_id] = {'id': node_id, 'text': text, 'children': [], 'type': 'category'}

    append_pattern = re.compile(r'_([A-Z0-9]+)\.appendChild\(_([A-Z0-9]+)_li\)')
    for match in append_pattern.finditer(js_text):
        parent_id = match.group(1)
        child_id = match.group(2)
        if parent_id in nodes and child_id in nodes:
            if nodes[child_id] not in nodes[parent_id]['children']:
                nodes[parent_id]['children'].append(nodes[child_id])
                
    chart_pattern = re.compile(r'\$\(_([A-Z0-9]+)_li\)\.html\([\'"](.*?)href=[\'"]/myaccident-content\?chartNo=(.*?)&chartType=\d+.*?<span[^>]*>.*?</span>(.*?)</a>', re.IGNORECASE | re.DOTALL)
    
    chart_vars = {}
    for match in chart_pattern.finditer(js_text):
        var_id = match.group(1)
        chart_no = urllib.parse.unquote(match.group(3))
        text = match.group(4).strip()
        
        node = {'id': var_id, 'chartNo': chart_no, 'text': text, 'type': 'chart', 'chartType': chart_type}
        chart_vars[var_id] = node

    for match in append_pattern.finditer(js_text):
        parent_id = match.group(1)
        child_id = match.group(2)
        if parent_id in nodes and child_id in chart_vars:
            nodes[parent_id]['children'].append(chart_vars[child_id])

    return root_nodes

def extract_chart_detail(chartNo, chartType):
    url = f"https://accident.knia.or.kr/myaccident-content?chartNo={urllib.parse.quote(chartNo)}&chartType={chartType}"
    html = fetch_url(url)
    if not html: return None
    
    soup = BeautifulSoup(html, 'html.parser')
    detail = {'chartNo': chartNo, 'factors': []}
    
    title_box = soup.select_one('.stit_box p.tit')
    if title_box:
        detail['title'] = title_box.get_text(strip=True)
    else:
        detail['title'] = f"{chartNo} 상세내용"
    
    video_source = soup.select_one('source[type="video/mp4"]')
    if video_source and video_source.get('src'):
        detail['videoUrl'] = "https://accident.knia.or.kr" + video_source['src']
    else:
        detail['imageUrl'] = f"https://accident.knia.or.kr/images/capture/{urllib.parse.quote(chartNo)}_case1.PNG" 
        
    # Extract tabs
    tab_situation = soup.select_one('#smrizeexplna')
    if tab_situation: detail['tab_situation'] = tab_situation.encode_contents().decode('utf-8', errors='replace')
    
    tab_apply = soup.select_one('#macont06')
    if tab_apply: detail['tab_apply'] = tab_apply.encode_contents().decode('utf-8', errors='replace')
    
    tab_explain = soup.select_one('#macont07')
    if tab_explain: detail['tab_explain'] = tab_explain.encode_contents().decode('utf-8', errors='replace')

    # Extract multiple cases
    cases = []
    default_acc = soup.find('tr', id='default_accident')
    if default_acc:
        tds = default_acc.find_all('td', recursive=False)
        case_ids = [td.get('id') for td in tds if 'tit' in td.get('class', [])]
        ratio_tds = [td for td in tds if 'tit' not in td.get('class', [])]
        
        car_tds = []
        car_row = soup.find('tr', id='caracdsittn')
        if car_row:
            car_tds = [td for td in car_row.find_all('td', recursive=False) if 'tit' not in td.get('class', [])]

        for idx, cid in enumerate(case_ids):
            case_data = {
                'id': cid,
                'label': '',
                'ratio_a': 0,
                'ratio_b': 0,
                'car_a_text': '',
                'car_b_text': '',
                'factors': []
            }
            
            if idx < len(ratio_tds):
                rtd = ratio_tds[idx]
                case_label = rtd.find('p', class_='case')
                if case_label: case_data['label'] = case_label.get_text(strip=True)
                red = rtd.find(class_='red')
                orange = rtd.find(class_='orange')
                if red: case_data['ratio_a'] = int(''.join(filter(str.isdigit, red.get_text())) or 0)
                if orange: case_data['ratio_b'] = int(''.join(filter(str.isdigit, orange.get_text())) or 0)
                
            if idx < len(car_tds):
                ctd = car_tds[idx]
                divs = ctd.find_all('div')
                for div in divs:
                    txt = div.get_text(strip=True)
                    if 'A :' in txt or 'A:' in txt or 'A차량' in txt or '자동차A' in txt:
                        case_data['car_a_text'] = txt.split(':', 1)[1].strip() if ':' in txt else txt
                    if 'B :' in txt or 'B:' in txt or 'B차량' in txt or '자동차B' in txt:
                        case_data['car_b_text'] = txt.split(':', 1)[1].strip() if ':' in txt else txt
            
            scr_con = soup.find('div', class_='scr_con', id=cid)
            if scr_con:
                for cb in scr_con.find_all(attrs={"data-a": True}):
                    label_el = cb.find_next_sibling('label')
                    label_txt = label_el.get_text(strip=True) if label_el else ''
                    case_data['factors'].append({
                        'label': label_txt,
                        'val_a': int(cb.get('data-a', 0)),
                        'val_b': int(cb.get('data-b', 0))
                    })
            
            cases.append(case_data)

    if cases:
        detail['cases'] = cases
        detail['ratio_a'] = cases[0]['ratio_a']
        detail['ratio_b'] = cases[0]['ratio_b']
        detail['factors'] = cases[0]['factors']
        detail['car_a_text'] = cases[0]['car_a_text']
        detail['car_b_text'] = cases[0]['car_b_text']
    else:
        # Fallback for older formats if no cases found
        a_score_span = soup.find(id='case1_a_score')
        b_score_span = soup.find(id='case1_b_score')
        if a_score_span and 'data-score' in a_score_span.attrs:
            detail['ratio_a'] = int(a_score_span['data-score'])
        if b_score_span and 'data-score' in b_score_span.attrs:
            detail['ratio_b'] = int(b_score_span['data-score'])
        
        a_con = soup.select_one('#case1 .cont_l .con')
        if a_con: detail['car_a_text'] = a_con.get_text(strip=True)
        b_con = soup.select_one('#case1 .cont_r .con')
        if b_con: detail['car_b_text'] = b_con.get_text(strip=True)
        
        for factor in soup.find_all(attrs={"data-a": True}):
            parent = factor.find_parent('td')
            if parent:
                detail['factors'].append({
                    'label': parent.get_text(strip=True),
                    'val_a': int(factor.get('data-a', '0')),
                    'val_b': int(factor.get('data-b', '0'))
                })

    return detail

def main():
    data = { 'details': {} }
    charts_to_fetch = []
    
    def find_charts(nodes):
        for n in nodes:
            if n['type'] == 'chart':
                charts_to_fetch.append(n)
            elif 'children' in n:
                find_charts(n['children'])
    
    # Mapping KNIA URL index to UI tree name and category name
    # 1: Car vs Car -> tree1
    # 2: Highway -> append to tree1
    # 3: Car vs Pedestrian -> tree2
    # 4: Car vs Two-Wheeler -> tree3
    # 5: Car vs Bicycle -> tree4
    knia_mapping = {
        1: ("tree1", "자동차 vs 자동차"),
        2: ("tree_highway", "고속도로"),
        3: ("tree2", "자동차 vs 보행자"),
        4: ("tree3", "자동차 vs 이륜차"),
        5: ("tree4", "자동차 vs 자전거")
    }

    for knia_idx, (tree_key, name) in knia_mapping.items():
        print(f"Scraping {name} (myaccident{knia_idx})...")
        html = fetch_url(f'https://accident.knia.or.kr/myaccident{knia_idx}')
        if not html:
            print(f"Failed to fetch myaccident{knia_idx}")
            data[tree_key] = []
            continue
        tree = parse_tree_from_html(html, knia_idx)
        data[tree_key] = tree

    # Merge Highway into tree1
    if 'tree_highway' in data and data['tree_highway']:
        if 'tree1' not in data: data['tree1'] = []
        highway_node = {'id': 'highway_merged', 'text': '고속도로/자동차전용도로', 'children': data['tree_highway'], 'type': 'category'}
        data['tree1'].append(highway_node)
        del data['tree_highway']
    
    # Collect all charts
    for tree_key in ['tree1', 'tree2', 'tree3', 'tree4']:
        if tree_key in data:
            find_charts(data[tree_key])

    total_charts = len(charts_to_fetch)
    print(f"Found a total of {total_charts} charts.")
    
    for i, c in enumerate(charts_to_fetch):
        print(f"Fetching detail for {c['chartNo']} ({i+1}/{total_charts})...")
        detail = extract_chart_detail(c['chartNo'], c['chartType'])
        if detail:
            data['details'][c['chartNo']] = detail
        delay = random.uniform(1.0, 2.0)
        print(f"Waiting {delay:.2f} seconds to avoid IP block...")
        time.sleep(delay)
        
    with open('accident_data.js', 'w', encoding='utf-8') as f:
        f.write('window.ACCIDENT_DATA_ASYNC = ')
        json.dump(data, f, ensure_ascii=False)
        f.write(';\n')
        
    print("Scraping complete. Saved to accident_data.js")

if __name__ == "__main__":
    main()
