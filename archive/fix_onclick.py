import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'r', 'utf-8').read()
text = text.replace("onclick=\"event.preventDefault(); navigateTo('view-disability-period')\"", "onclick=\"navigateTo('view-disability-period'); return false;\"")
codecs.open('c:/Users/SB/Desktop/연습용/index.html', 'w', 'utf-8').write(text)
print("Fixed onclick handlers")
