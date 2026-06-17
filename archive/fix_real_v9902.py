import codecs
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# 1. Delete the first v9902_life (from line 29)
first_v9902_idx = script.find('"v9902_life": {')
second_v9902_idx = script.find('"v9902_life": {', first_v9902_idx + 10)

if second_v9902_idx != -1:
    # There are two! Let's delete the first one.
    # We need to find where the first one ends. It ends when the next key starts, or at the end of the object.
    # The first one is at the beginning of allDisabilityData. 
    # Let's find the comma that separates the first one from the next one.
    # The next one is probably "v9502_life_9901" or something.
    next_key_idx = script.find('v9502_life_9901: {', first_v9902_idx)
    # But wait, v9502 is at the end of the file.
    # Is there a key right after the first v9902_life?
    
    # Actually, it's safer to just extract the second v9902_life, and the rest of the file.
    # Let's just find the second v9902_life, which is the REAL one.
    real_start = second_v9902_idx
    real_end = script.find('v9502_life_9901: {', real_start)
    if real_end == -1:
        # maybe it ends with };
        real_end = len(script)
        
    real_v9902_text = script[real_start:real_end]
    
    # 2. Modify the parts array of the real v9902_life
    parts_start = real_v9902_text.find('parts: [')
    parts_end = real_v9902_text.find('explanations: [', parts_start)
    
    if parts_start != -1 and parts_end != -1:
        parts_text = real_v9902_text[parts_start:parts_end]
        
        def replace_rate(match):
            desc = match.group(1) 
            rate = match.group(2) 
            
            # Extract m from "m. 텍스트" or " m. 텍스트"
            m_match = re.match(r'^\s*(\d+)\.', desc)
            if m_match and "항" not in rate:
                m = m_match.group(1)
                new_rate = f"{rate}{m}항"
                return f'{{ desc: "{desc}", rate: "{new_rate}" }}'
            return match.group(0)

        new_parts_text = re.sub(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', replace_rate, parts_text)
        
        new_real_v9902_text = real_v9902_text[:parts_start] + new_parts_text + real_v9902_text[parts_end:]
        
        # Now replace the real v9902 in the script
        script = script[:real_start] + new_real_v9902_text + script[real_end:]
        
        codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script)
        print("Successfully updated the real v9902_life parts!")
    else:
        print("Could not find parts or explanations in the real v9902_life")
else:
    print("Could not find two v9902_life instances")

