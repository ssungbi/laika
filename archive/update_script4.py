import os

script_path = r"C:\Users\SB\Desktop\연습용\script.js"

with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: class view layout
old_class_li = """                    <li style="padding: 12px; border-bottom: 1px solid #f1f5f9;">
                        <div class="dis-desc" style="font-size: 15px; color: #334155; line-height: 1.5;">
                            <span style="font-weight:bold; color:#2563eb; margin-right:12px; display:inline-block; min-width:85px; white-space:nowrap;">[${item.part}]</span>
                            ${item.desc}
                        </div>
                    </li>"""
new_class_li = """                    <li style="padding: 12px; border-bottom: 1px solid #f1f5f9; display: flex; align-items: flex-start;">
                        <span style="font-weight:bold; color:#2563eb; margin-right:12px; min-width:85px; white-space:nowrap; flex-shrink: 0; margin-top: 2px;">[${item.part}]</span>
                        <div class="dis-desc" style="font-size: 15px; color: #334155; line-height: 1.5; flex: 1;">${item.desc}</div>
                    </li>"""
content = content.replace(old_class_li, new_class_li)

# Fix 2: part view layout
old_part_li = """                    <li style="padding: 12px; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center;">
                        <div class="dis-rate" style="font-weight:700; color:#ef4444; margin-right: 16px; white-space: nowrap; min-width: 45px;">${item.grade}</div>
                        <div class="dis-desc" style="font-size: 15px; color: #334155; line-height: 1.5; flex: 1;">${item.desc}</div>
                    </li>"""
new_part_li = """                    <li style="padding: 12px; border-bottom: 1px solid #f1f5f9; display: flex; align-items: flex-start;">
                        <div class="dis-rate" style="font-weight:700; color:#ef4444; margin-right: 16px; white-space: nowrap; min-width: 45px; flex-shrink: 0; margin-top: 2px;">${item.grade}</div>
                        <div class="dis-desc" style="font-size: 15px; color: #334155; line-height: 1.5; flex: 1;">${item.desc}</div>
                    </li>"""
content = content.replace(old_part_li, new_part_li)


# Fix search highlight logic to also highlight the new span structure
old_search_logic = """                    const lis = acc.querySelectorAll('li, .dis-desc, > div > div');"""
new_search_logic = """                    const lis = acc.querySelectorAll('li, .dis-desc, span, .dis-rate, .accordion-body > div');"""
content = content.replace(old_search_logic, new_search_logic)

with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied flex layout fixes to script.js")
