import json

log_path = 'C:/Users/SB/.gemini/antigravity-ide/brain/17a1464f-3ef5-458a-ae24-c2d47b439041/.system_generated/logs/transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('tool_calls'):
            for tc in obj['tool_calls']:
                if 'args' in tc:
                    for k, v in tc['args'].items():
                        if isinstance(v, str) and '"v9902_life": {' in v and len(v) > 5000:
                            with open('c:/Users/SB/Desktop/연습용/script_recovered.js', 'w', encoding='utf-8') as out:
                                out.write(v)
