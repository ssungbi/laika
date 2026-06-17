import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
text = text.replace('styles.css?v=5', 'styles.css?v=6')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Bumped css to v=6")
