import json
import codecs

largest_script = ""

with codecs.open('c:/Users/SB/Desktop/연습용/test.txt', 'r', 'utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line.strip())
            
            # Check content
            if 'content' in entry and isinstance(entry['content'], str):
                if '"v1804": [' in entry['content']:
                    if len(entry['content']) > len(largest_script):
                        largest_script = entry['content']
            
            # Check tool calls
            if 'tool_calls' in entry:
                for tc in entry['tool_calls']:
                    args = tc.get('arguments', {})
                    for arg_name, arg_val in args.items():
                        if isinstance(arg_val, str) and '"v1804": [' in arg_val:
                            if len(arg_val) > len(largest_script):
                                largest_script = arg_val
                                
            # Check tool responses
            if 'tool_responses' in entry:
                for tr in entry['tool_responses']:
                    if tr.get('response') and isinstance(tr['response'], dict):
                        out = tr['response'].get('output', '')
                        if '"v1804": [' in out and len(out) > len(largest_script):
                            largest_script = out
        except Exception as e:
            pass

print(f"Found largest chunk of size {len(largest_script)}")
if len(largest_script) > 50000:
    codecs.open('c:/Users/SB/Desktop/연습용/recovered_full.txt', 'w', 'utf-8').write(largest_script)
    print("Saved to recovered_full.txt")
