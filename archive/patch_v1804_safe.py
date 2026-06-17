import codecs
import json
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
latest_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/latest_data_media.json', 'r', 'utf-8'))
latest_json_str = json.dumps(latest_data, ensure_ascii=False, indent=4)

pattern = r'("v1804"\s*:\s*\[\s*\{.*?)(?=\n};\n\nconst tooltipKeywords)'
match = re.search(pattern, script_text, flags=re.DOTALL)
if match:
    new_str = f'"v1804": {latest_json_str}'
    script_text = script_text[:match.start()] + new_str + script_text[match.end():]
    codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
    print("Replaced v1804 block successfully!")
else:
    # Try another pattern, since earlier it might not have been an array but an object
    pattern2 = r'("v1804"\s*:\s*\{.*?)(?=\n};\n\nconst tooltipKeywords)'
    match2 = re.search(pattern2, script_text, flags=re.DOTALL)
    if match2:
        new_str = f'"v1804": {latest_json_str}'
        script_text = script_text[:match2.start()] + new_str + script_text[match2.end():]
        codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
        print("Replaced v1804 block successfully (pattern 2)!")
    else:
        # Just find the last "v1804": 
        # Since it's the last key in allDisabilityData
        idx = script_text.rfind('"v1804":')
        end_idx = script_text.find('};\n\nconst tooltipKeywords_v9807', idx)
        if idx != -1 and end_idx != -1:
            new_str = f'"v1804": {latest_json_str}\n'
            script_text = script_text[:idx] + new_str + script_text[end_idx:]
            codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
            print("Replaced v1804 block successfully using index!")
        else:
            print("Could not find the bounds.")
