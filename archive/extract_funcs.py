import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# Let's find each function and extract it.
funcs = {}
for func_name in ['navigateTo', 'toggleAccordion', 'switchDtTab', 'applyTooltips', 'jumpToExp', 'loadDisabilityTable']:
    start = text.find(f'function {func_name}')
    if start != -1:
        # find the end of the function (rough heuristic: count braces)
        brace_count = 0
        in_func = False
        for i in range(start, len(text)):
            if text[i] == '{':
                brace_count += 1
                in_func = True
            elif text[i] == '}':
                brace_count -= 1
                if in_func and brace_count == 0:
                    funcs[func_name] = text[start:i+1]
                    break

print("Extracted functions:", list(funcs.keys()))

# Also find tooltipKeywords
tk_start = text.find('const tooltipKeywords')
if tk_start != -1:
    tk_end = text.find('};', tk_start) + 2
    funcs['tooltipKeywords'] = text[tk_start:tk_end]

# What about allDisabilityData? It's currently messed up.
# But wait, earlier I saved `dump_v9902_parts.js`!
# Let's see if I have the clean grades_9902_utf8.json and parsed_9902.json
