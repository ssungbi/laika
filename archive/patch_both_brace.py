import codecs
import json

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

def patch_version(text, version_key, json_file):
    data = json.load(codecs.open(json_file, 'r', 'utf-8'))
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    json_str = "\n".join("    " + line for line in json_str.split("\n"))

    start_marker = f'"{version_key}": {{'
    start_idx = text.find(start_marker)

    if start_idx != -1:
        brace_count = 0
        end_idx = -1
        for i in range(start_idx + len(f'"{version_key}": '), len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
                    
        if end_idx != -1:
            new_block = f'"{version_key}": {json_str.strip()}'
            text = text[:start_idx] + new_block + text[end_idx:]
            print(f"Replaced {version_key} block successfully!")
            return text
        else:
            print(f"Could not find matching brace for {version_key}.")
            return text
    else:
        print(f"Could not find {version_key} start marker.")
        return text

script_text = patch_version(script_text, 'v0505_unified', 'c:/Users/SB/Desktop/연습용/v0505_data_adls.json')
script_text = patch_version(script_text, 'v1804', 'c:/Users/SB/Desktop/연습용/latest_data_media5.json')

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
