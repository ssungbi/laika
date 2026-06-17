import codecs

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8').read()

# 1. Remove the dangling v9902_life at the end
start_idx = script.rfind('    "v9902_life": {')
if start_idx != -1:
    v9902_str = script[start_idx:]
    script = script[:start_idx]
    
    # 2. Insert it before v9502_life_9901
    insert_idx = script.find('v9502_life_9901: {')
    if insert_idx != -1:
        new_script = script[:insert_idx] + v9902_str.strip() + ',\n    ' + script[insert_idx:]
        codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8').write(new_script)
        print("Fixed script.js successfully!")
    else:
        print("Could not find v9502_life_9901: {")
else:
    print("Could not find v9902_life at the end")
