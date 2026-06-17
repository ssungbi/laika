import codecs

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx1 = 856
idx2 = 44673

print("--- FIRST ---")
print(script[idx1:idx1+200])
print("--- SECOND ---")
print(script[idx2:idx2+200])
