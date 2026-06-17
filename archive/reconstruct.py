import codecs
import json

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# find v9902_life string
start_idx = script.find('"v9902_life": {')
if start_idx == -1:
    start_idx = script.find('v9902_life: {')

# The end of v9902_life is right before the end of allDisabilityData, which is the last '}'
# Let's extract the whole v9902_life object text.
# We know script.js currently only contains v9902_life.
v9902_text = script[start_idx:]
# Find the closing brace of allDisabilityData
last_brace = v9902_text.rfind('}')
v9902_text = v9902_text[:last_brace]
# Strip trailing commas
v9902_text = v9902_text.strip().rstrip(',')

# create v9502_life_9901 by replacing the key
v9502_text = v9902_text.replace('"v9902_life": {', '"v9502_life_9901": {')
v9502_text = v9502_text.replace('v9902_life: {', '"v9502_life_9901": {')
# also replace the title? v9902_life doesn't have a title field, it's injected by loadDisabilityTable.

# Add placeholders for deleted data
placeholders = """
    "v1804": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
    "v0505": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
    "v8310_life": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
    "v9807_nonlife": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
    "vPre9807_nonlife": [{ category: "복구 중", items: [{ desc: "데이터가 유실되어 복구 중입니다.", rate: "-" }] }],
"""

# Now assemble allDisabilityData
new_all = "const allDisabilityData = {\n" + placeholders + v9502_text + ",\n" + v9902_text + "\n};"

# replace allDisabilityData in script
all_start = script.find('const allDisabilityData = {')
all_end = script.find('};', all_start) + 2

new_script = script[:all_start] + new_all + script[all_end:]

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(new_script)
print("Reconstructed script.js with v9502_life_9901 and placeholders.")
