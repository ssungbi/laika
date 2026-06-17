import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx = text.find('const tooltipKeywords_v9807')
print(text[idx-200:idx+50])
