import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# 1. Extract functions
funcs = []
for func_name in ['navigateTo', 'toggleAccordion', 'switchDtTab', 'applyTooltips', 'jumpToExp', 'loadDisabilityTable']:
    start = text.find(f'function {func_name}')
    if start != -1:
        brace_count = 0
        in_func = False
        for i in range(start, len(text)):
            if text[i] == '{':
                brace_count += 1
                in_func = True
            elif text[i] == '}':
                brace_count -= 1
                if in_func and brace_count == 0:
                    funcs.append(text[start:i+1])
                    break

tk_start = text.find('const tooltipKeywords')
if tk_start != -1:
    tk_end = text.find('};', tk_start) + 2
    funcs.insert(0, text[tk_start:tk_end])

# 2. Extract v9902_life CLEANLY
v9902_start = text.find('"v9902_life": {')
if v9902_start == -1:
    v9902_start = text.find('v9902_life: {')

exp_start = text.find('explanations: [', v9902_start)
# find the end of explanations array
brace_count = 0
in_arr = False
for i in range(exp_start, len(text)):
    if text[i] == '[':
        brace_count += 1
        in_arr = True
    elif text[i] == ']':
        brace_count -= 1
        if in_arr and brace_count == 0:
            # The end of explanations array is at i
            # The v9902_life object ends after this array, probably with a '}'
            # Let's find the next '}'
            obj_end = text.find('}', i)
            v9902_clean = text[v9902_start:obj_end+1]
            break

# 3. Create v9502_life_9901 from v9902_clean
v9502_clean = v9902_clean.replace('"v9902_life": {', '"v9502_life_9901": {')
v9502_clean = v9502_clean.replace('v9902_life: {', '"v9502_life_9901": {')

# 4. Build allDisabilityData
placeholders = """
    "v1804": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
    "v0505": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
    "v8310_life": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
    "v9807_nonlife": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
    "vPre9807_nonlife": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
"""

all_data = f"""const allDisabilityData = {{
{placeholders}
{v9502_clean},
{v9902_clean}
}};
"""

# 5. Assemble new script.js
new_script = "\n\n".join(funcs) + "\n\n" + all_data

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(new_script)
print("Rebuilt script.js completely and cleanly.")
