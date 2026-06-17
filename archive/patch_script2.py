import codecs
import re

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

new_logic = """} else if (data.type === 'tab' || data.type === 'parts_only' || data.type === 'parts_and_exp') {
        const partsContainer = document.getElementById('disability-parts');
        
        if (data.type === 'parts_only') {
            tabs.classList.add('hidden'); // Hide the entire tab bar
        } else {
            tabs.classList.remove('hidden');
            const tabBtns = document.querySelectorAll('.dt-tab');
            if (data.type === 'parts_and_exp') {
                tabBtns[0].classList.add('hidden'); // Hide Grades tab
                tabBtns[1].classList.remove('hidden');
                tabBtns[1].classList.add('active'); // Activate Parts tab
                tabBtns[2].classList.remove('hidden');
                tabBtns[2].classList.remove('active');
            } else {
                tabBtns[0].classList.remove('hidden');
                tabBtns[0].classList.add('active'); // Activate Grades tab
                tabBtns[1].classList.remove('hidden');
                tabBtns[1].classList.remove('active');
                tabBtns[2].classList.remove('hidden');
                tabBtns[2].classList.remove('active');
            }
        }
        
        desc.classList.add('hidden');
        
        if (data.type === 'parts_only' || data.type === 'parts_and_exp') {
            container.classList.add('hidden');
            partsContainer.classList.remove('hidden');
            expContainer.classList.add('hidden'); // Default is parts view
        } else {
            container.classList.remove('hidden');
            partsContainer.classList.add('hidden');
            expContainer.classList.add('hidden');
        }

        // 1."""

pattern = r'\} else if \(data\.type === \'tab\' \|\| data\.type === \'parts_only\'\) \{[\s\S]*?(?=\s*// 1\.)'
script_text = re.sub(pattern, new_logic.strip(), script_text, count=1)

# Fix the final else block to hide partsContainer
# The else block looks like:
#     } else {
#         tabs.classList.add('hidden');
#         expContainer.classList.add('hidden');
#         container.classList.remove('hidden');
#         desc.classList.remove('hidden');

final_else_fix = """    } else {
        const partsContainer = document.getElementById('disability-parts');
        if (partsContainer) partsContainer.classList.add('hidden');
        tabs.classList.add('hidden');
        expContainer.classList.add('hidden');
        container.classList.remove('hidden');
        desc.classList.remove('hidden');"""

pattern2 = r'\} else \{\s*tabs\.classList\.add\(\'hidden\'\);\s*expContainer\.classList\.add\(\'hidden\'\);\s*container\.classList\.remove\(\'hidden\'\);\s*desc\.classList\.remove\(\'hidden\'\);'
script_text = re.sub(pattern2, final_else_fix, script_text, count=1)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated loadDisabilityTable with parts_and_exp and fix for final else block")
