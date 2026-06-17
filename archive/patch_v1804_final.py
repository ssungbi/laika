import codecs
import json
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
latest_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/latest_data_media.json', 'r', 'utf-8'))
latest_json_str = json.dumps(latest_data, ensure_ascii=False, indent=4)

idx = script_text.find('const tooltipKeywords_v9807')
if idx != -1:
    # Find the closing brace of allDisabilityData
    brace_idx = script_text.rfind('};', 0, idx)
    v1804_idx = script_text.rfind('"v1804":', 0, brace_idx)
    
    if brace_idx != -1 and v1804_idx != -1:
        new_str = f'"v1804": {latest_json_str}\n'
        script_text = script_text[:v1804_idx] + new_str + script_text[brace_idx:]
        codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
        print("Replaced v1804 block successfully!")
    else:
        print("Could not find brace or v1804.")
else:
    print("Could not find tooltipKeywords_v9807.")
