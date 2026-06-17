import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
text = text.replace('script.js?v=11', 'script.js?v=12')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Bumped version to v=12")
