import codecs
import re

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

start_idx = script.find('"v9902_life": {')
end_idx = script.find('v9502_life_9901: {')

v9902_text = script[start_idx:end_idx]

# We want to ONLY modify the `parts:` array inside `v9902_life`
# The `parts:` array starts at `parts: [` and ends at `explanations: [`
parts_start = v9902_text.find('parts: [')
parts_end = v9902_text.find('explanations: [', parts_start)

if parts_start != -1 and parts_end != -1:
    parts_text = v9902_text[parts_start:parts_end]
    
    # We will replace `{ desc: "m. ...", rate: "n급" }` with `rate: "n급m항"`
    def replace_rate(match):
        desc = match.group(1) # e.g. "1. 두 눈의 ..."
        rate = match.group(2) # e.g. "1급"
        
        # extract m from desc
        m_match = re.match(r'^(\d+)\.', desc)
        if m_match and "항" not in rate:
            m = m_match.group(1)
            new_rate = f"{rate}{m}항"
            return f'{{ desc: "{desc}", rate: "{new_rate}" }}'
        return match.group(0)

    # regex to match: { desc: "...", rate: "..." }
    new_parts_text = re.sub(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', replace_rate, parts_text)
    
    new_v9902_text = v9902_text[:parts_start] + new_parts_text + v9902_text[parts_end:]
    script = script[:start_idx] + new_v9902_text + script[end_idx:]
    
    codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script)
    print("Modified v9902_life parts successfully!")
else:
    print("Could not find parts or explanations in v9902_life")

