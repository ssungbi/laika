import os

script_path = r"C:\Users\SB\Desktop\연습용\script.js"

with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: selector error in filterInjury
old_selector = "const lis = acc.querySelectorAll('li, .dis-desc, > div > div');"
new_selector = "const lis = acc.querySelectorAll('li, .dis-desc, .accordion-body > div');"
content = content.replace(old_selector, new_selector)

# Fix 2: min-width for category
old_class_li = """<span style="font-weight:bold; color:#2563eb; margin-right:8px; display:inline-block; min-width:60px;">[${item.part}]</span>"""
new_class_li = """<span style="font-weight:bold; color:#2563eb; margin-right:12px; display:inline-block; min-width:85px; white-space:nowrap;">[${item.part}]</span>"""
content = content.replace(old_class_li, new_class_li)

# Fix 3: swap grade and desc in part view
old_part_li = """                    <li style="padding: 12px; border-bottom: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center;">
                        <div class="dis-desc" style="font-size: 15px; color: #334155; line-height: 1.5; flex: 1;">${item.desc}</div>
                        <div class="dis-rate" style="font-weight:700; color:#ef4444; margin-left: 16px; white-space: nowrap;">${item.grade}</div>
                    </li>"""

new_part_li = """                    <li style="padding: 12px; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center;">
                        <div class="dis-rate" style="font-weight:700; color:#ef4444; margin-right: 16px; white-space: nowrap; min-width: 45px;">${item.grade}</div>
                        <div class="dis-desc" style="font-size: 15px; color: #334155; line-height: 1.5; flex: 1;">${item.desc}</div>
                    </li>"""
content = content.replace(old_part_li, new_part_li)

with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixes applied to script.js")
