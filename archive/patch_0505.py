import codecs
import json

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

v0505_data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/v0505_data.json', 'r', 'utf-8'))
v0505_json_str = json.dumps(v0505_data, ensure_ascii=False, indent=8)

# Find "v0505_unified":
start_idx = script_text.find('"v0505_unified":')
if start_idx == -1:
    # Look for "v0505":
    start_idx = script_text.find('"v0505":')
    if start_idx == -1:
        print("Could not find v0505_unified or v0505 in script.js")
        exit(1)

# Find the end of the current object
brace_count = 0
in_obj = False
end_idx = -1
for i in range(start_idx, len(script_text)):
    if script_text[i] == '{' or script_text[i] == '[':
        brace_count += 1
        in_obj = True
    elif script_text[i] == '}' or script_text[i] == ']':
        brace_count -= 1
        if in_obj and brace_count == 0:
            end_idx = i
            break

if end_idx != -1:
    new_script = script_text[:start_idx] + '"v0505_unified": ' + v0505_json_str + script_text[end_idx+1:]
    
    # Wait, in the tooltip logic, we need to disable tooltips for v0505_unified as well?
    # Yes, the user wants the same layout as v9807_nonlife (no tooltips, just bottom box).
    if "versionId === 'v9807_nonlife'" in new_script:
        new_script = new_script.replace("if (versionId === 'v9807_nonlife') return text;", "if (versionId === 'v9807_nonlife' || versionId === 'v0505_unified') return text;")
    
    codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(new_script)
    print("Patched script.js with v0505_unified data!")
else:
    print("Could not find end of v0505 object")

