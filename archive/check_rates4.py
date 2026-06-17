import codecs
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx1 = script.find('v9502_life_9901')
idx2 = script.find('parts: [', idx1)
idx3 = script.find('explanations: [', idx2)
rates = re.findall(r'"rate":\s*"([^"]+)"', script[idx2:idx3])
unmapped = [r for r in rates if r == '-']
print(f"Total parts rates: {len(rates)}")
print(f"Unmapped rates (-): {len(unmapped)}")
