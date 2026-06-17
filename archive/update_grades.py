import codecs
import json

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()
grades_data = codecs.open('c:/Users/SB/Desktop/연습용/grades_9902_full.json', 'r', 'utf-8').read()

def replace_grades(text, version_key):
    start = text.find(f'"{version_key}": {{')
    if start == -1:
        start = text.find(f'{version_key}: {{')
    if start == -1: return text
    
    g_start = text.find('grades: [', start)
    g_end = text.find('parts: [', g_start)
    
    if g_start == -1 or g_end == -1: return text
    
    # We replace from g_start to g_end with `grades: [ ... JSON ... ],\n`
    # But grades_data is `[ ... ]`. We need `grades: [\n ... \n],\n`
    # Actually grades_data is the exact array string!
    new_grades = "grades: " + grades_data + ",\n        "
    
    # Find the exact start of `parts: [` by walking backwards from g_end to avoid replacing `parts: [`
    # Well, text[g_start:g_end] will replace `grades: [...],` and stop exactly at `parts: [` which is perfect
    return text[:g_start] + new_grades + text[g_end:]

script = replace_grades(script, "v9902_life")
script = replace_grades(script, "v9502_life_9901")

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script)
print("Updated script.js with FULL grades!")
