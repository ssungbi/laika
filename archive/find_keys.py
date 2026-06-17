import codecs
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
keys = re.findall(r'v[0-9a-z_]+:', script)
print(keys)
