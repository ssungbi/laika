import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
text = text.replace('script.js?v=14', 'script.js?v=15')
text = text.replace('styles.css?v=3', 'styles.css?v=4')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Bumped version to v=15 and css to v=4")
