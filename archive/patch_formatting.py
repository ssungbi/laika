import codecs
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# 1. Add formatExplanationContent function
formatter_func = """
function formatExplanationContent(content) {
    let text = Array.isArray(content) ? content.join('\\n') : content;
    text = text.replace(/<br\\s*\\/?>/gi, '\\n');
    
    let lines = text.split('\\n');
    let formatted = lines.map(line => {
        let trimmed = line.trim();
        if (!trimmed) return '';
        
        let plainText = trimmed.replace(/<[^>]+>/g, '').trim();
        
        let pad = 0;
        let indent = 0;
        let margin = 0;
        let top = 2;
        let bottom = 2;
        
        if (/^①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩/.test(plainText)) {
            pad = 15; indent = -15; margin = 15;
        } else if (/^[가-하]\\./.test(plainText)) {
            pad = 0; indent = 0; margin = 0; top = 12; bottom = 4;
        } else if (/^[가-하]\\)/.test(plainText)) {
            pad = 30; indent = -15; margin = 15;
        } else if (/^㉮|㉯|㉰|㉱|㉲|㉳/.test(plainText)) {
            pad = 45; indent = -15; margin = 15;
        } else if (/^-/.test(plainText)) {
            pad = 15; indent = -10; margin = 10;
        } else if (/^\\d+\\)/.test(plainText)) {
            pad = 0; indent = -15; margin = 15; top = 6;
        } else {
            pad = 0; indent = 0; margin = 0;
        }
        
        return `<div style="padding-left: ${pad}px; text-indent: ${indent}px; margin-left: ${margin}px; margin-top: ${top}px; margin-bottom: ${bottom}px;">${trimmed}</div>`;
    });
    
    return formatted.join('');
}
"""

if "function formatExplanationContent" not in script_text:
    # insert before applyTooltips
    script_text = script_text.replace("function applyTooltips", formatter_func + "\nfunction applyTooltips")

# 2. Replace the old render logic
script_text = script_text.replace("expData.content.replace(/\\n/g, '<br>')", "formatExplanationContent(expData.content)")
script_text = script_text.replace("exp.content.replace(/\\n/g, '<br>')", "formatExplanationContent(exp.content)")
script_text = script_text.replace("chongData.content.replace(/\\n/g, '<br>')", "formatExplanationContent(chongData.content)")
script_text = script_text.replace("crData.content.replace(/\\n/g, '<br>')", "formatExplanationContent(crData.content)")
script_text = script_text.replace("adlsData.content.replace(/\\n/g, '<br>')", "formatExplanationContent(adlsData.content)")

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Formatting logic applied.")
