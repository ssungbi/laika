import json
import codecs
import re

def fix_eyes_in_data(data):
    for part in data.get('parts', []):
        if '1. 눈의 장해' in part['category']:
            for item in part['items']:
                desc = item['desc']
                if '0.06' in desc and desc.startswith('4)'):
                    item['desc'] = '4) 한 눈의 교정시력이 0.06 이하로 된 때'
                elif '0.1' in desc and desc.startswith('5)'):
                    item['desc'] = '5) 한 눈의 교정시력이 0.1 이하로 된 때'
                elif '0.2' in desc and desc.startswith('6)'):
                    item['desc'] = '6) 한 눈의 교정시력이 0.2 이하로 된 때'
    
    for group in data.get('grades', []):
        if '1. 눈의 장해' in group['category']:
            for item in group['items']:
                desc = item['desc']
                if '0.06' in desc and desc.startswith('4)'):
                    item['desc'] = '4) 한 눈의 교정시력이 0.06 이하로 된 때'
                elif '0.1' in desc and desc.startswith('5)'):
                    item['desc'] = '5) 한 눈의 교정시력이 0.1 이하로 된 때'
                elif '0.2' in desc and desc.startswith('6)'):
                    item['desc'] = '6) 한 눈의 교정시력이 0.2 이하로 된 때'
    return data

try:
    v0505_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/v0505_data_adls.json', 'r', 'utf-8'))
    v0505_data = fix_eyes_in_data(v0505_data)
    with codecs.open('c:/Users/SB/Desktop/연습용/v0505_data_adls.json', 'w', 'utf-8') as f:
        json.dump(v0505_data, f, ensure_ascii=False, indent=4)
    print("Fixed v0505 adls JSON")
except Exception as e:
    print("Error v0505:", e)
