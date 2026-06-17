import json
import codecs

log_file = 'C:/Users/SB/.gemini/antigravity-ide/brain/17a1464f-3ef5-458a-ae24-c2d47b439041/.system_generated/logs/transcript.jsonl'
largest_script = ""

with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            # look in content or tool_calls
            if 'content' in entry and entry['content']:
                if '"v1804": [' in entry['content'] and len(entry['content']) > len(largest_script):
                    largest_script = entry['content']
            
            if 'tool_calls' in entry:
                for tc in entry['tool_calls']:
                    args = tc.get('arguments', {})
                    for arg_name, arg_val in args.items():
                        if isinstance(arg_val, str) and '"v1804": [' in arg_val:
                            if len(arg_val) > len(largest_script):
                                largest_script = arg_val
                                
            if 'tool_responses' in entry:
                for tr in entry['tool_responses']:
                    if tr.get('response') and isinstance(tr['response'], dict):
                        out = tr['response'].get('output', '')
                        if '"v1804": [' in out and len(out) > len(largest_script):
                            largest_script = out
        except Exception as e:
            pass

print(f"Found a script of length {len(largest_script)}")
if largest_script:
    codecs.open('c:/Users/SB/Desktop/연습용/recovered_full.txt', 'w', encoding='utf-8').write(largest_script)
    print("Saved to recovered_full.txt")
