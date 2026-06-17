import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/parsed_latest.txt', 'r', 'utf-8').read().splitlines()

with open('c:/Users/SB/Desktop/연습용/dump_repr.txt', 'w', encoding='utf-8') as f:
    f.write(repr(text[24]))
