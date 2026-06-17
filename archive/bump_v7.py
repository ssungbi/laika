import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
new_text = text.replace('script.js?v=6', 'script.js?v=7')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(new_text)
print("Bumped version to v=7")
