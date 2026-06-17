import codecs
import re

text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

rates = [
    # 눈
    "1급1항", "3급1항", "4급1항", "6급1항",
    # 귀
    "2급6항", "4급14항", "5급11항", "5급12항", "6급11항",
    # 코
    "5급13항",
    # 입
    "1급2항", "4급2항",
    # 추상
    "5급15항", "6급12항",
    # 척추
    "3급9항", "4급15항", "5급14항", "4급16항", "5급16항", "6급14항",
    # 팔다리 (5 + 2 + 5 + 3 + 2 + 3 = 20)
    "1급5항", "1급6항", "1급7항", "1급8항", "1급9항",
    "2급3항", "2급5항",
    "3급2항", "3급3항", "3급4항", "3급5항", "3급10항",
    "4급5항", "4급6항", "4급7항",
    "5급2항", "5급3항",
    "6급2항", "6급3항", "6급4항",
    # 손가락 (16)
    "2급4항",
    "3급6항", "3급7항",
    "4급8항", "4급9항",
    "4급10항", "4급11항",
    "5급4항", "5급5항", "5급6항", "5급7항", "5급8항",
    "6급5항", "6급6항", "6급7항", "6급8항",
    # 발가락 (7)
    "3급8항", "4급12항", "4급13항", "5급9항", "5급10항", "6급9항", "6급10항",
    # 흉복부 (5)
    "1급4항", "2급2항", "4급4항", "5급1항", "6급13항",
    # 정신 (3)
    "1급3항", "2급1항", "4급3항"
]

# Process v9902_life
idx_start = text.find('"v9902_life": {')
parts_start = text.find('parts: [', idx_start)
exp_start = text.find('explanations: [', parts_start)

parts_text = text[parts_start:exp_start]

# find all desc / rate pairs
def repl(m):
    global rate_idx
    desc = m.group(1)
    if rate_idx < len(rates):
        new_rate = rates[rate_idx]
        rate_idx += 1
        return f'{{ desc: "{desc}", rate: "{new_rate}" }}'
    return m.group(0)

rate_idx = 0
new_parts_text = re.sub(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', repl, parts_text)

# Process v9502_life_9901
idx2_start = text.find('"v9502_life_9901": {')
parts2_start = text.find('parts: [', idx2_start)
exp2_start = text.find('explanations: [', parts2_start)

parts2_text = text[parts2_start:exp2_start]

rate_idx = 0
new_parts2_text = re.sub(r'\{\s*desc:\s*"([^"]+)",\s*rate:\s*"([^"]+)"\s*\}', repl, parts2_text)

# Construct new script
new_script = text[:parts2_start] + new_parts2_text + text[exp2_start:parts_start] + new_parts_text + text[exp_start:]

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(new_script)
print("Updated exactly!")
