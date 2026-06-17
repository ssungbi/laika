import re

def format_explanation_content(text):
    lines = text.split('\n')
    formatted = []
    for line in lines:
        trimmed = line.strip()
        if not trimmed:
            continue
            
        plainText = re.sub(r'<[^>]+>', '', trimmed).strip()
        
        pad = 0
        indent = 0
        margin = 0
        top = 2
        bottom = 2
        
        if re.search(r'^[①②③④⑤⑥⑦⑧⑨⑩]', plainText):
            pad = 15
            indent = -15
            margin = 15
        elif re.search(r'^[가-하]\.', plainText):
            pad = 0
            indent = 0
            margin = 0
            top = 12
            bottom = 4
        elif re.search(r'^[가-하]\)', plainText):
            pad = 30
            indent = -15
            margin = 15
        elif re.search(r'^[㉮㉯㉰㉱㉲㉳]', plainText):
            pad = 45
            indent = -15
            margin = 15
        elif re.search(r'^-', plainText):
            pad = 15
            indent = -10
            margin = 10
        elif re.search(r'^\d+\)', plainText):
            pad = 0
            indent = -15
            margin = 15
            top = 6
        else:
            pad = 0
            indent = 0
            margin = 0
            
        formatted.append(f'<div style="padding-left: {pad}px; text-indent: {indent}px; margin-left: {margin}px; margin-top: {top}px; margin-bottom: {bottom}px;">{trimmed}</div>')
    return '\n'.join(formatted)

sample = """
4. 씹어먹거나 말하는 장해
1) 씹어먹는 기능의 장해는...
2) '씹어먹는 기능에...
5) '말하는 기능에 심한 장해를 남긴 때'라 함은 다음 4종의 어음 중 3종 이상의 발음을 할 수 없게 된 경우를 말한다.
① 양순음/입술소리(ㅁ, ㅂ, ㅍ)
② 치조음/잇몸소리(ㄴ, ㄷ, ㄹ)
"""
print(format_explanation_content(sample))
