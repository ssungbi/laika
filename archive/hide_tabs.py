import codecs
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

new_logic = """} else if (data.type === 'tab' || data.type === 'parts_only') {
        if (data.type === 'parts_only') {
            tabs.classList.add('hidden'); // Hide the entire tab bar since there's only one view
        } else {
            tabs.classList.remove('hidden');
            const tabBtns = document.querySelectorAll('.dt-tab');
            tabBtns[0].classList.remove('hidden');
            tabBtns[0].classList.add('active'); // Activate Grades tab
            tabBtns[1].classList.remove('hidden');
            tabBtns[1].classList.remove('active');
            tabBtns[2].classList.remove('active');
        }
        desc.classList.add('hidden');
        
        const partsContainer = document.getElementById('disability-parts');
        
        if (data.type === 'parts_only') {
            container.classList.add('hidden');
            partsContainer.classList.remove('hidden');
        } else {
            container.classList.remove('hidden');
            partsContainer.classList.add('hidden');
        }
        
        expContainer.classList.add('hidden');

        // 1."""

pattern = r'\} else if \(data\.type === \'tab\' \|\| data\.type === \'parts_only\'\) \{[\s\S]*?(?=\s*// 1\.)'
script_text = re.sub(pattern, new_logic.strip(), script_text, count=1)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated script.js to hide tabs entirely for parts_only")
