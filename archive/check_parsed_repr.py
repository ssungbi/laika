import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/parsed_0505.txt', 'r', 'utf-8').read()
idx = text.find('양순음')
snippet = text[max(0, idx-50):idx+50]

with open('c:/Users/SB/Desktop/연습용/dump_repr.txt', 'w', encoding='utf-8') as f:
    f.write(repr(snippet))
