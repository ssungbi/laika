import json
import codecs

log_path = 'C:/Users/SB/.gemini/antigravity-ide/brain/17a1464f-3ef5-458a-ae24-c2d47b439041/.system_generated/logs/transcript.jsonl'

longest_match = ""
max_len = 0

with codecs.open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
        except:
            continue
            
        if obj.get('tool_calls'):
            for tc in obj['tool_calls']:
                if 'args' in tc:
                    for k, v in tc['args'].items():
                        if isinstance(v, str):
                            if '"v9902_life":' in v or "'v9902_life':" in v:
                                if len(v) > max_len:
                                    max_len = len(v)
                                    longest_match = v

if longest_match:
    with codecs.open('c:/Users/SB/Desktop/연습용/recovered_full.txt', 'w', encoding='utf-8') as out:
        out.write(longest_match)
    print("Found and wrote %d bytes" % max_len)
else:
    print("Not found")
