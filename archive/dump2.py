import codecs
text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
v_start = text.find('explanations: [', text.find('"v9807_nonlife": {'))
v_end = text.find(']', v_start)
block = text[v_start:v_end+500]
codecs.open('c:/Users/SB/Desktop/연습용/temp_dump2.txt', 'w', 'utf-8').write(block)
