import codecs

css_text = codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'r', 'utf-8').read()
css_text = css_text.replace(
    '.exp-content ol { padding-left: 20px; margin-top: 4px; margin-bottom: 4px; }', 
    '.exp-content ol { padding-left: 20px; margin-top: 4px; margin-bottom: 4px; list-style-type: none; }'
)
css_text = css_text.replace(
    '.exp-content ul { padding-left: 20px; margin-top: 4px; margin-bottom: 4px; }', 
    '.exp-content ul { padding-left: 20px; margin-top: 4px; margin-bottom: 4px; list-style-type: none; }'
)
codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'w', 'utf-8').write(css_text)
print("Added list-style-type: none to exp-content lists!")
