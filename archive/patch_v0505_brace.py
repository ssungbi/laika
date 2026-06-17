import codecs
import json

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
v0505_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/v0505_data_adls.json', 'r', 'utf-8'))
v0505_json_str = json.dumps(v0505_data, ensure_ascii=False, indent=4)
v0505_json_str = "\n".join("    " + line for line in v0505_json_str.split("\n"))

start_marker = '"v0505_unified": {'
start_idx = script_text.find(start_marker)

if start_idx != -1:
    brace_count = 0
    end_idx = -1
    for i in range(start_idx + len('"v0505_unified": '), len(script_text)):
        if script_text[i] == '{':
            brace_count += 1
        elif script_text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
                
    if end_idx != -1:
        new_v0505 = f'"v0505_unified": {v0505_json_str.strip()}'
        script_text = script_text[:start_idx] + new_v0505 + script_text[end_idx:]
        codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
        print("Replaced v0505_unified block successfully!")
    else:
        print("Could not find matching brace.")
else:
    print("Could not find v0505_unified start marker.")
