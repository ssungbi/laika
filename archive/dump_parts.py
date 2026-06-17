import codecs
import json
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# get v9902_life object
idx = text.find('"v9902_life"')
s = text[idx:text.find('explanations:', idx)]

with codecs.open('c:/Users/SB/Desktop/연습용/dump_v9902_parts.js', 'w', 'utf-8') as f:
    f.write("var v9902 = {" + s + "explanations: []};")
