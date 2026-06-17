import codecs
text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx = text.find('"v9902_life": {')
print(text[idx-500:idx+500])
