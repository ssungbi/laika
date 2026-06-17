import json
with open('c:/Users/SB/Desktop/연습용/accident_data.js', 'r', encoding='utf-8') as f:
    text = f.read().replace('window.ACCIDENT_DATA_ASYNC = ', '').strip().rstrip(';')
data = json.loads(text)
for k, v in data['details'].items():
    if 'videoUrl' in v:
        print(f'{k}: {v["videoUrl"]}')
        break
