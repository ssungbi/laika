import codecs
import json
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# Find the v9807_nonlife explanations block
v_start = script_text.find('"v9807_nonlife": {')
if v_start != -1:
    exp_start = script_text.find('explanations: [', v_start)
    if exp_start != -1:
        # find the end of the explanations array
        brace_count = 0
        in_arr = False
        exp_end = -1
        for j in range(exp_start + len('explanations: '), len(script_text)):
            if script_text[j] == '[':
                brace_count += 1
                in_arr = True
            elif script_text[j] == ']':
                brace_count -= 1
                if in_arr and brace_count == 0:
                    exp_end = j
                    break
        if exp_end != -1:
            exp_json_str = script_text[exp_start + len('explanations: '):exp_end+1]
            try:
                explanations = json.loads(exp_json_str)
                for exp in explanations:
                    # Remove all newlines and tabs from the HTML content
                    exp["content"] = re.sub(r'[\n\t\r]+', '', exp["content"])
                
                new_exp_json_str = json.dumps(explanations, ensure_ascii=False, indent=8)
                script_text = script_text[:exp_start] + f"explanations: {new_exp_json_str}" + script_text[exp_end+1:]
                
                codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
                print("Removed whitespace from v9807_nonlife explanations!")
            except Exception as e:
                print("Error parsing JSON:", e)

# Also let's tighten the CSS margins for p and ol inside exp-content
css_text = codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'r', 'utf-8').read()
css_text = css_text.replace('.exp-content ol { padding-left: 20px; margin-top: 8px; margin-bottom: 8px; }', '.exp-content ol { padding-left: 20px; margin-top: 4px; margin-bottom: 4px; }')
css_text = css_text.replace('.exp-content ul { padding-left: 20px; margin-top: 8px; margin-bottom: 8px; }', '.exp-content ul { padding-left: 20px; margin-top: 4px; margin-bottom: 4px; }')
css_text = css_text.replace('.exp-content p { margin-top: 4px; margin-bottom: 4px; }', '.exp-content p { margin-top: 2px; margin-bottom: 2px; }')
codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'w', 'utf-8').write(css_text)
print("Updated CSS margins!")

