import codecs

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

start_idx = script_text.find('if (data.explanations && data.explanations.length > 0) {')
end_idx = script_text.find('} else {', start_idx + 1000)

codecs.open('c:/Users/SB/Desktop/연습용/dump_exp.txt', 'w', 'utf-8').write(script_text[start_idx:end_idx+200])
