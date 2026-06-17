import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
new_text = text.replace('script.js?v=4', 'script.js?v=5')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(new_text)
print("Bumped version to v=5")
