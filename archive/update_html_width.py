import os

html_path = r"C:\Users\SB\Desktop\연습용\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace max-width: 800px with max-width: 1200px in the injury view section
old_tabs = """<div style="display: flex; gap: 10px; margin-bottom: 24px; max-width: 800px; margin-left: auto; margin-right: auto;">"""
new_tabs = """<div style="display: flex; gap: 10px; margin-bottom: 24px; max-width: 1200px; margin-left: auto; margin-right: auto;">"""
content = content.replace(old_tabs, new_tabs)

old_search = """<div class="insurance-search-container" style="max-width: 800px; margin: 0 auto 24px auto; position: relative;">"""
new_search = """<div class="insurance-search-container" style="max-width: 1200px; margin: 0 auto 24px auto; position: relative;">"""
content = content.replace(old_search, new_search)

old_view_class = """<div id="injury-view-class" style="display: block; max-width: 800px; margin: 0 auto;" class="accordion-group">"""
new_view_class = """<div id="injury-view-class" style="display: block; max-width: 1200px; margin: 0 auto;" class="accordion-group">"""
content = content.replace(old_view_class, new_view_class)

old_view_part = """<div id="injury-view-part" style="display: none; max-width: 800px; margin: 0 auto;" class="accordion-group">"""
new_view_part = """<div id="injury-view-part" style="display: none; max-width: 1200px; margin: 0 auto;" class="accordion-group">"""
content = content.replace(old_view_part, new_view_part)

old_view_guide = """<div id="injury-view-guide" style="display: none; max-width: 800px; margin: 0 auto;" class="accordion-group">"""
new_view_guide = """<div id="injury-view-guide" style="display: none; max-width: 1200px; margin: 0 auto;" class="accordion-group">"""
content = content.replace(old_view_guide, new_view_guide)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html to 1200px width")
