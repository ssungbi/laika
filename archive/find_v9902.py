import codecs

lines = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').readlines()
for i, line in enumerate(lines):
    if '"v9902_life"' in line:
        print(f"Line {i+1}: {line.strip()}")
