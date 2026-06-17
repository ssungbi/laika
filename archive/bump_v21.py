import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
text = text.replace('script.js?v=20', 'script.js?v=21')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Bumped script to v=21")
