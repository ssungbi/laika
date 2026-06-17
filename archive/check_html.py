import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
idx = text.find('id="view-disability-period"')
print(text[max(0, idx-300):idx+300])
