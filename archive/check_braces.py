import sys
import os

try:
    with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
        data = f.read()
except Exception as e:
    print(f"Failed to read: {e}")
    sys.exit(1)

# we can use Python's ast to check if it has gross matching of braces
stack = []
for i, c in enumerate(data):
    if c in '{[':
        stack.append((c, i))
    elif c in '}]':
        if not stack:
            print(f"Unmatched closing '{c}' at index {i}")
            sys.exit(1)
        top_c, top_i = stack.pop()
        if (c == '}' and top_c != '{') or (c == ']' and top_c != '['):
            print(f"Mismatched '{c}' at index {i}, matches '{top_c}' at index {top_i}")
            sys.exit(1)

if stack:
    print(f"Unclosed '{stack[-1][0]}' at index {stack[-1][1]}")
else:
    print("Braces and brackets matched perfectly!")
