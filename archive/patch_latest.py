import codecs
import json

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
latest_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/latest_data.json', 'r', 'utf-8'))
latest_json_str = json.dumps(latest_data, ensure_ascii=False, indent=4)

old_v1804_marker = '"v1804": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],'
new_v1804_str = f'"v1804": {latest_json_str},'

if old_v1804_marker in script_text:
    script_text = script_text.replace(old_v1804_marker, new_v1804_str)
    codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
    print("Replaced v1804 in script.js successfully!")
else:
    print("Could not find the v1804 placeholder in script.js")
