import codecs

with codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8') as f:
    for i, line in enumerate(f):
        if 'tab-btn' in line:
            print(f"{i}: {line.strip()}")
