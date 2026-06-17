import codecs
import json

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
latest_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/latest_data_media2.json', 'r', 'utf-8'))
latest_json_str = json.dumps(latest_data, ensure_ascii=False, indent=4)
latest_json_str = "\n".join("    " + line for line in latest_json_str.split("\n"))

start_marker = '"v1804": {'
start_idx = script_text.find(start_marker)

if start_idx != -1:
    brace_count = 0
    end_idx = -1
    for i in range(start_idx + len('"v1804": '), len(script_text)):
        if script_text[i] == '{':
            brace_count += 1
        elif script_text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
                
    if end_idx != -1:
        new_v1804 = f'"v1804": {latest_json_str.strip()}'
        script_text = script_text[:start_idx] + new_v1804 + script_text[end_idx:]
        codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
        print("Replaced v1804 block successfully!")
    else:
        print("Could not find matching brace.")
else:
    print("Could not find v1804 start marker.")
