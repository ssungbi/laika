import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/blocks_debug.txt', 'r', 'utf-8').read().splitlines()
with codecs.open('c:/Users/SB/Desktop/연습용/blocks_debug_clean.txt', 'w', 'utf-8') as f:
    for line in text[25:40]:
        f.write(line + '\n')
