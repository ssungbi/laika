import codecs
import json
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
latest_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/latest_data_media.json', 'r', 'utf-8'))
latest_json_str = json.dumps(latest_data, ensure_ascii=False, indent=4)

# Replace the "v1804": { ... } block
# It's at the end of allDisabilityData, just before };
new_str = f'"v1804": {latest_json_str}\n}};'
script_text = re.sub(r'"v1804":\s*\{.*?\n};\s*$', new_str, script_text, flags=re.DOTALL)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Replaced v1804 block successfully!")
