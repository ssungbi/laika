import sys

try:
    with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
        data = f.read()
except Exception as e:
    print(f"Failed to read: {e}")
    sys.exit(1)

# let's strip comments first, roughly, to not get confused by quotes in comments
# then check quotes
def check_syntax(s):
    in_str = None
    escape = False
    
    for i, c in enumerate(s):
        if in_str:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == in_str:
                # end of string
                in_str = None
        else:
            if c in '"\'`':
                in_str = c
    if in_str:
        print(f"Unclosed string {in_str} at end of file!")
        return False
    return True

if check_syntax(data):
    print("Strings matched perfectly!")
