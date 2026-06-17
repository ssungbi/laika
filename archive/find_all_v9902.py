import codecs
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
matches = [m.start() for m in re.finditer(r'"v9902_life"', script)]
print("v9902_life found at:", matches)
