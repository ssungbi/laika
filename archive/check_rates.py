import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx = text.find('"v9902_life"')
s = text[idx:text.find('explanations:', idx)]
rates = re.findall(r'rate:\s*"([^"]+)"', s)
print(rates)
