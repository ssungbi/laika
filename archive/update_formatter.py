import codecs
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

old_func = """function formatExplanationContent(content) {
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
}"""

new_func = """function formatExplanationContent(content) {
    let text = Array.isArray(content) ? content.join('\\n') : content;
    text = text.replace(/<br\\s*\\/?>/gi, '\\n');
    
    // Also split by \n or any block tags if needed, but we already have newlines
    let lines = text.split('\\n');
    let formatted = lines.map(line => {
        let trimmed = line.trim();
        if (!trimmed) return '';
        
        // Remove HTML entities and tags for pure text testing
        let plainText = trimmed.replace(/&nbsp;/g, ' ').replace(/<[^>]+>/g, '').trim();
        
        let pad = 0;
        let indent = 0;
        let margin = 0;
        let top = 2;
        let bottom = 2;
        
        // 1) 2) ... : Base level
        if (/^\\d+\\)/.test(plainText)) {
            pad = 0; indent = -24; margin = 24; top = 8;
        } 
        // ① ② ... : Level 1 indent (under numbers)
        else if (/^[①②③④⑤⑥⑦⑧⑨⑩]/.test(plainText)) {
            pad = 24; indent = -20; margin = 24;
        } 
        // 가) 나) ... : Level 2 indent
        else if (/^[가-하]\\)/.test(plainText)) {
            pad = 44; indent = -20; margin = 24;
        } 
        // ㉮ ㉯ ... : Level 3 indent
        else if (/^[㉮㉯㉰㉱㉲㉳]/.test(plainText)) {
            pad = 64; indent = -20; margin = 24;
        } 
        // - : Level 1 bullet
        else if (/^-/.test(plainText)) {
            pad = 24; indent = -16; margin = 24;
        }
        // 가. 나. : Top level title
        else if (/^[가-하]\\./.test(plainText)) {
            pad = 0; indent = 0; margin = 0; top = 16; bottom = 6;
        } 
        else {
            pad = 0; indent = 0; margin = 0;
        }
        
        return `<div style="display: block; padding-left: ${pad}px; text-indent: ${indent}px; margin-left: ${margin}px; margin-top: ${top}px; margin-bottom: ${bottom}px;">${trimmed}</div>`;
    });
    
    return formatted.join('');
}"""

script_text = script_text.replace(old_func, new_func)
codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated formatting logic in script.js.")
