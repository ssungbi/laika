import codecs
text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
idx = text.find('view-disability-period', text.find('onclick') + 100)
print(text[idx-100:idx+300])
