import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
text = text.replace('script.js?v=15', 'script.js?v=16')
text = text.replace('styles.css?v=4', 'styles.css?v=5')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Bumped version to v=16 and css to v=5")
