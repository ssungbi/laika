import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# Check v9502_life_9901
idx1 = text.find('"v9502_life_9901": {')
idx2 = text.find('"v9902_life": {')

v9502_text = text[idx1:idx2]
v9902_text = text[idx2:]

def print_rates(name, block):
    parts_idx = block.find('parts: [')
    if parts_idx == -1:
        print(f"No parts found in {name}")
        return
    exp_idx = block.find('explanations: [', parts_idx)
    parts_text = block[parts_idx:exp_idx]
    rates = re.findall(r'rate:\s*"([^"]+)"', parts_text)
    print(f"{name} parts rates (first 20):", rates[:20])

print_rates("v9502_life_9901", v9502_text)
print_rates("v9902_life", v9902_text)
