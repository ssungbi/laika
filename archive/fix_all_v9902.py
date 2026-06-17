import codecs
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# 1. Find and remove the duplicate first v9902_life
first_idx = script.find('"v9902_life": {')
# The next key should be "v1804": [
next_key_idx = script.find('"v1804": [', first_idx)

if first_idx != -1 and next_key_idx != -1:
    script = script[:first_idx] + script[next_key_idx:]
    print("Removed duplicate first v9902_life")
else:
    print("Could not find duplicate v9902_life or next key")

# 2. Find the real v9902_life (which is now the only one, or we can just search again)
start_idx = script.find('"v9902_life": {')
end_idx = script.find('v9502_life_9901: {')

if start_idx != -1 and end_idx != -1:
    v9902_text = script[start_idx:end_idx]

    parts_start = v9902_text.find('parts: [')
    parts_end = v9902_text.find('explanations: [', parts_start)

    if parts_start != -1 and parts_end != -1:
        parts_text = v9902_text[parts_start:parts_end]
        
        def replace_rate(match):
            desc = match.group(1) 
            rate = match.group(2) 
            
            m_match = re.match(r'^(\d+)\.', desc)
            if m_match and "항" not in rate:
                m = m_match.group(1)
                new_rate = f"{rate}{m}항"
                return f'{{ desc: "{desc}", rate: "{new_rate}" }}'
            return match.group(0)

        new_parts_text = re.sub(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', replace_rate, parts_text)
        
        new_v9902_text = v9902_text[:parts_start] + new_parts_text + v9902_text[parts_end:]
        script = script[:start_idx] + new_v9902_text + script[end_idx:]
        
        codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script)
        print("Modified real v9902_life parts successfully!")
    else:
        print("Could not find parts or explanations in real v9902_life")
else:
    print("Could not find real v9902_life")
