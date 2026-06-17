import json
import codecs

def fix_eyes_in_data(data):
    for part in data.get('parts', []):
        if '1. 눈의 장해' in part['category']:
            for item in part['items']:
                if item['desc'] == '4) " 0.06 "':
                    item['desc'] = '4) 한 눈의 교정시력이 0.06 이하로 된 때'
                elif item['desc'] == '5) " 0.1 "':
                    item['desc'] = '5) 한 눈의 교정시력이 0.1 이하로 된 때'
                elif item['desc'] == '6) " 0.2 "':
                    item['desc'] = '6) 한 눈의 교정시력이 0.2 이하로 된 때'
    
    # Also check the grades array if it exists (for v1804 Grades tab)
    for group in data.get('grades', []):
        if '1. 눈의 장해' in group['category']:
            for item in group['items']:
                if item['desc'] == '4) " 0.06 "':
                    item['desc'] = '4) 한 눈의 교정시력이 0.06 이하로 된 때'
                elif item['desc'] == '5) " 0.1 "':
                    item['desc'] = '5) 한 눈의 교정시력이 0.1 이하로 된 때'
                elif item['desc'] == '6) " 0.2 "':
                    item['desc'] = '6) 한 눈의 교정시력이 0.2 이하로 된 때'
    return data

# Fix v1804
try:
    v1804_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/latest_data_media5.json', 'r', 'utf-8'))
    v1804_data = fix_eyes_in_data(v1804_data)
    with codecs.open('c:/Users/SB/Desktop/연습용/latest_data_media5.json', 'w', 'utf-8') as f:
        json.dump(v1804_data, f, ensure_ascii=False, indent=4)
    print("Fixed v1804")
except Exception as e:
    print("Error v1804:", e)

# Fix v0505
try:
    v0505_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/v0505_data_adls.json', 'r', 'utf-8'))
    v0505_data = fix_eyes_in_data(v0505_data)
    with codecs.open('c:/Users/SB/Desktop/연습용/v0505_data_adls.json', 'w', 'utf-8') as f:
        json.dump(v0505_data, f, ensure_ascii=False, indent=4)
    print("Fixed v0505")
except Exception as e:
    print("Error v0505:", e)
