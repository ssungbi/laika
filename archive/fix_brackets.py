import codecs
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# 1. Fix '))' to ')'
script_text = script_text.replace(')) ', ') ')

# 2. Disable tooltips for v9807_nonlife
# In applyTooltips, if versionId === 'v9807_nonlife', just return text!
disable_tooltips_code = """function applyTooltips(text, versionId) {
    if (versionId === 'v9807_nonlife') return text; // Disable tooltips for this version
    
    let result = text;
    let currentKeywords = tooltipKeywords;"""

script_text = re.sub(r'function applyTooltips\(text, versionId\) \{\s*let result = text;\s*let currentKeywords = tooltipKeywords;\s*if \(versionId === \'v9807_nonlife\'\) \{\s*currentKeywords = tooltipKeywords_v9807;\s*\}', disable_tooltips_code, script_text)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Fixed script.js (replaced )) and disabled tooltips for v9807)")

# 3. Update styles.css for .part-exp-item-content so it handles HTML properly without pre-wrap issues
css_text = codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'r', 'utf-8').read()

# Change white-space: pre-wrap to normal so HTML tags render without extra newlines, 
# although we already stripped \n from v9807 explanations, so pre-wrap is fine,
# but let's apply the same ol/ul/p margin rules to part-exp-item-content just in case!
css_patch = """
.part-exp-item-content ol { padding-left: 20px; margin-top: 4px; margin-bottom: 4px; list-style-type: none; }
.part-exp-item-content ul { padding-left: 20px; margin-top: 4px; margin-bottom: 4px; list-style-type: none; }
.part-exp-item-content p { margin-top: 2px; margin-bottom: 2px; }
"""
if '.part-exp-item-content ol' not in css_text:
    css_text += css_patch
    
# also remove white-space: pre-wrap from .part-exp-item-content if we want to be clean,
# but other versions might need it. We'll leave it since we stripped \n in v9807.
codecs.open('c:/Users/SB/Desktop/연습용/styles.css', 'w', 'utf-8').write(css_text)
print("Updated styles.css for part-exp-item-content HTML support")
