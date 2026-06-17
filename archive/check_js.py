import codecs

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

idx = script_text.find('function formatExplanationContent')
print(script_text[idx:idx+1500])
