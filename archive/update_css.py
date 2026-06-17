import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'r', 'utf-8').read()
text = text.replace('.accordion-group {\n    display: flex;\n    flex-direction: column;\n    gap: 12px;\n}', 
                    '.accordion-group {\n    display: flex;\n    flex-direction: column;\n    gap: 20px;\n}')

codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'w', 'utf-8').write(text)
print("Updated styles.css gap")
