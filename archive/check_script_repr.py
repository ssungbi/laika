import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx = text.find('formatExplanationContent')
snippet = text[max(0, idx+200):idx+500]

with open('c:/Users/SB/Desktop/연습용/dump_repr.txt', 'w', encoding='utf-8') as f:
    f.write(repr(snippet))
