import json
import re
import codecs

data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/v9902_life_data.json', 'r', encoding='utf-8'))

# Fix exp 21
for exp in data['explanations']:
    if exp['id'] == 'exp21':
        idx = exp['content'].find('.<br>function')
        if idx != -1:
            exp['content'] = exp['content'][:idx+1]

# Now let's read script.js to grab the 'parts' from v9502_life_9901
script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8').read()

parts_match = re.search(r'parts:\s*\[(.*?)\]\s*,\s*explanations:', script, re.DOTALL)
if parts_match:
    parts_str = parts_match.group(1)
    
    # We need to add 추상장해 (part 11) to parts_str for 99.02
    # Wait, the user said: "4. 우리 부위가 11개인거자나 그럼 11개로 바꾸고 7,9 빠진것은 제외 하고 1~11로 작성해줘"
    # So 11 parts. 1. 눈 2. 귀 3. 코 ... 
    # For now, let's just use the parts_str from 9502, but add 11. 추상장해
    추상장해_part = """
            {
                category: "11. 추상장해",
                items: [
                    { desc: "1. 두부 및 안면부에 현저한 추상을 남겼을 때", rate: "5급15항" },
                    { desc: "2. 두부 및 안면부에 추상을 남겼을 때", rate: "6급12항" }
                ],
                expIndices: [16]
            }"""
    parts_str += "," + 추상장해_part

# Format v9902_life string
v9902_str = '    "v9902_life": {\n'
v9902_str += '        type: "tab",\n'
v9902_str += '        grades: [\n'

for grade in data['grades']:
    if not grade['items']: continue
    v9902_str += '            {\n'
    v9902_str += f'                category: "{grade["category"]}",\n'
    v9902_str += '                items: [\n'
    items_str = []
    for item in grade['items']:
        desc = item['desc'].replace('"', '\\"')
        items_str.append(f'                    {{ desc: "{desc}", rate: "{item["rate"]}" }}')
    v9902_str += ',\n'.join(items_str) + '\n'
    v9902_str += '                ]\n'
    v9902_str += '            },\n'

v9902_str = v9902_str.rstrip(',\n') + '\n        ],\n'
v9902_str += '        parts: [\n' + parts_str + '\n        ],\n'

v9902_str += '        explanations: [\n'
for exp in data['explanations']:
    title = exp['title'].replace('"', '\\"')
    content = exp['content'].replace('"', '\\"')
    v9902_str += '            {\n'
    v9902_str += f'                id: "{exp["id"]}",\n'
    v9902_str += f'                title: "{title}",\n'
    v9902_str += f'                content: "{content}"\n'
    v9902_str += '            },\n'
v9902_str = v9902_str.rstrip(',\n') + '\n        ]\n    },\n'

# Insert v9902_life into script.js before v9502_life_9901
insert_idx = script.find('"v9502_life_9901": {')
new_script = script[:insert_idx] + v9902_str + script[insert_idx:]

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8').write(new_script)
print("Successfully recovered and inserted v9902_life!")
