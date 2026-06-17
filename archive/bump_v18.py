import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
text = text.replace('script.js?v=16', 'script.js?v=17')
text = text.replace('styles.css?v=6', 'styles.css?v=7')
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Bumped script to v=17 and css to v=7")
