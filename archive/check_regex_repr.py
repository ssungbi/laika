import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx = text.find('if (/^')
snippet = text[max(0, idx):idx+100]

with open('c:/Users/SB/Desktop/연습용/dump_repr.txt', 'w', encoding='utf-8') as f:
    f.write(repr(snippet))
