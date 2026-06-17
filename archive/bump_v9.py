import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
text = text.replace('styles.css?v=2', 'styles.css?v=3')
text = text.replace('script.js?v=8', 'script.js?v=9')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Bumped version to v=9 and css to v=3")
