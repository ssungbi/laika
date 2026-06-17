import codecs
text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
idx = text.find('id="view-disability-period"')
print(text[idx-50:idx+300])
