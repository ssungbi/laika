import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
keys = re.findall(r'"v[0-9a-z_]+"\s*:', text)
print("KEYS in script.js:", keys)
