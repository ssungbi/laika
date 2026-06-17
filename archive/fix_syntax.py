import codecs

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

bad_comment = """    // Also split by 
 or any block tags if needed, but we already have newlines"""
good_comment = "    // Also split by \\n or any block tags if needed, but we already have newlines"

script_text = script_text.replace(bad_comment, good_comment)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Fixed syntax error")
