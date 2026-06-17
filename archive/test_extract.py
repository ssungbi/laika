from bs4 import BeautifulSoup
import json

with open('c:/Users/SB/Desktop/연습용/debug_1_2.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

cases = []

# Find all cases from default_accident header
default_acc = soup.find('tr', id='default_accident')
if default_acc:
    # First td is the row title, the rest are cases
    tds = default_acc.find_all('td', recursive=False)
    # The first few might be '.tit', like <td id="case1">, <td id="case2">
    case_ids = []
    case_labels = []
    for td in tds:
        if 'tit' in td.get('class', []):
            case_ids.append(td.get('id'))
    
    # The ratios are in the subsequent tds
    ratio_tds = [td for td in tds if 'tit' not in td.get('class', [])]
    
    # caracdsittn tds for car names
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
        
        # Parse ratio
        if idx < len(ratio_tds):
            rtd = ratio_tds[idx]
            case_label = rtd.find('p', class_='case')
            if case_label: case_data['label'] = case_label.get_text(strip=True)
            red = rtd.find(class_='red')
            orange = rtd.find(class_='orange')
            if red: case_data['ratio_a'] = int(''.join(filter(str.isdigit, red.get_text())) or 0)
            if orange: case_data['ratio_b'] = int(''.join(filter(str.isdigit, orange.get_text())) or 0)
            
        # Parse car texts
        if idx < len(car_tds):
            ctd = car_tds[idx]
            divs = ctd.find_all('div')
            for div in divs:
                txt = div.get_text(strip=True)
                if 'A :' in txt or 'A:' in txt or 'A차량' in txt or '자동차A' in txt:
                    case_data['car_a_text'] = txt.split(':', 1)[1].strip() if ':' in txt else txt
                if 'B :' in txt or 'B:' in txt or 'B차량' in txt or '자동차B' in txt:
                    case_data['car_b_text'] = txt.split(':', 1)[1].strip() if ':' in txt else txt
        
        # Parse factors
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

with open('c:/Users/SB/Desktop/연습용/test_cases_out.json', 'w', encoding='utf-8') as f:
    json.dump(cases, f, indent=2, ensure_ascii=False)
