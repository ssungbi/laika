import codecs

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
idx = text.rfind('"v1804":')
# Find the next 'const ' which signifies the end of the allDisabilityData object
end_idx = text.find('\nconst ', idx)
if end_idx != -1:
    print(text[end_idx-100:end_idx+50])
