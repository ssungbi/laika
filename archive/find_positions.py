import codecs

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
print("v9902:", script.find('"v9902_life": {'))
print("v9502:", script.find('v9502_life_9901: {'))
