import codecs
import json
import re

data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/grades_9902_full.json', 'r', 'utf-8'))

for g in data:
    for item in g['items']:
        desc = item['desc']
        # remove trailing >
        desc = desc.replace('>', '')
        # remove `<SPAN...`
        desc = re.sub(r'<[A-Z].*', '', desc)
        # remove extra spaces
        desc = re.sub(r'\s+', ' ', desc).strip()
        item['desc'] = desc

codecs.open('c:/Users/SB/Desktop/연습용/grades_9902_full.json', 'w', 'utf-8').write(json.dumps(data, ensure_ascii=False, indent=4))
print("Cleaned JSON")
