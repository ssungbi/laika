import codecs
import json
import re

html = codecs.open('c:/Users/SB/Desktop/연습용/user_9807_data.html', 'r', 'utf-8').read()
parts_html, exp_html = html.split('---')

# We only need to fix Explanations, Parts was correct.
# Wait, let's load current script.js and just update explanations array for v9807_nonlife.
script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

explanations = []
# General notes
general_notes = re.findall(r'<li>(.*?)</li>', exp_html.split('<p>&lt;용어풀이&gt;</p>')[0], re.DOTALL)
for i, note in enumerate(general_notes):
    clean_note = re.sub(r'<[^>]+>', '', note).strip()
    if clean_note:
        explanations.append({
            "title": f"일반사항 {i+1}",
            "content": clean_note
        })

# 용어풀이 (Terms)
terms_html = exp_html.split('<p>&lt;용어풀이&gt;</p>')[1]

# To properly parse the top-level <li> elements and preserve their inner HTML
# Let's find the first <ol>
ol_start = terms_html.find('<ol>')
ol_end = terms_html.rfind('</ol>')
inner_ol = terms_html[ol_start+4:ol_end]

# We need to split by top-level <li>
# Since there are nested <ol><li>, we should count <ol> and <li> tags to find the top level.
top_level_items = []
current_item = ""
depth_ol = 0
i = 0
while i < len(inner_ol):
    if inner_ol[i:i+4] == '<ol>':
        depth_ol += 1
        current_item += '<ol>'
        i += 4
    elif inner_ol[i:i+5] == '</ol>':
        depth_ol -= 1
        current_item += '</ol>'
        i += 5
    elif inner_ol[i:i+4] == '<li>' and depth_ol == 0:
        # Start of a new top-level item
        if current_item.strip():
            top_level_items.append(current_item.strip())
        current_item = ""
        i += 4
    elif inner_ol[i:i+5] == '</li>' and depth_ol == 0:
        # End of top-level item
        if current_item.strip():
            top_level_items.append(current_item.strip())
        current_item = ""
        i += 5
    else:
        current_item += inner_ol[i]
        i += 1

if current_item.strip():
    top_level_items.append(current_item.strip())

for item_html in top_level_items:
    # item_html contains the text for the title and the nested html
    # Usually the title is the first text node or up to the first block tag like <p> or <ol>
    # Let's split at the first <p> or <ol>
    match = re.search(r'(<p>|<ol>)', item_html)
    if match:
        idx = match.start()
        title_raw = item_html[:idx].strip()
        content_raw = item_html[idx:].strip()
    else:
        title_raw = item_html.strip()
        content_raw = ""
    
    # clean up title
    title_clean = re.sub(r'<[^>]+>', '', title_raw).strip()
    # It might have a number at the start, e.g. "1. 귓바퀴의 대부분의 결손"
    # Wait, the original HTML just has "귓바퀴의 대부분의 결손" without the number!
    # Because it was in an <ol>, the browser added the number.
    # We should add the number back since our JS renders them as standalone cards.
    
    # Actually, let's just use the title as is.
    
    explanations.append({
        "title": title_clean,
        "content": content_raw
    })

# Add numbering to the term titles starting from index 4
for i in range(4, len(explanations)):
    explanations[i]["title"] = f"{i-3}. {explanations[i]['title']}"

# Update the script.js explanations array for v9807_nonlife
# We will just replace the "explanations": [...] block inside v9807_nonlife
import json
exp_str = json.dumps(explanations, ensure_ascii=False, indent=8)

# Find the v9807_nonlife block
v_start = script_text.find('"v9807_nonlife": {')
if v_start != -1:
    exp_start = script_text.find('explanations: [', v_start)
    if exp_start != -1:
        # find the end of the explanations array
        brace_count = 0
        in_arr = False
        exp_end = -1
        for j in range(exp_start + len('explanations: '), len(script_text)):
            if script_text[j] == '[':
                brace_count += 1
                in_arr = True
            elif script_text[j] == ']':
                brace_count -= 1
                if in_arr and brace_count == 0:
                    exp_end = j
                    break
        if exp_end != -1:
            script_text = script_text[:exp_start] + f"explanations: {exp_str}" + script_text[exp_end+1:]

# Wait, the content HTML might have <p> and <ol> tags.
# If we just dump it, the browser will render it perfectly.
# Also, we should add some CSS styling for <ol> and <ul> inside exp-content to look nice.
css_patch = """
.exp-content ol { padding-left: 20px; margin-top: 8px; margin-bottom: 8px; }
.exp-content ul { padding-left: 20px; margin-top: 8px; margin-bottom: 8px; }
.exp-content p { margin-top: 4px; margin-bottom: 4px; }
"""
styles_text = codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'r', 'utf-8').read()
if '.exp-content ol' not in styles_text:
    styles_text += css_patch
    codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'w', 'utf-8').write(styles_text)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated explanations for 9807 to preserve HTML!")
