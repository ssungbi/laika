import codecs

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# 1. Update loadDisabilityTable
old_else_if = "    } else if (data.type === 'tab') {"
new_logic = """    } else if (data.type === 'tab' || data.type === 'parts_only') {
        tabs.classList.remove('hidden');
        desc.classList.add('hidden');
        
        const tabBtns = document.querySelectorAll('.dt-tab');
        if (data.type === 'parts_only') {
            tabBtns[0].classList.add('hidden'); // Hide Grades tab
            tabBtns[1].classList.add('active'); // Activate Parts tab
            tabBtns[1].classList.remove('hidden');
            tabBtns[2].classList.remove('active');
        } else {
            tabBtns[0].classList.remove('hidden');
            tabBtns[0].classList.add('active'); // Activate Grades tab
            tabBtns[1].classList.remove('hidden');
            tabBtns[1].classList.remove('active');
            tabBtns[2].classList.remove('active');
        }
        
        const partsContainer = document.getElementById('disability-parts');
        
        if (data.type === 'parts_only') {
            container.classList.add('hidden');
            partsContainer.classList.remove('hidden');
        } else {
            container.classList.remove('hidden');
            partsContainer.classList.add('hidden');
        }
        
        expContainer.classList.add('hidden');

        // 1. 급수별 렌더링 (if tab)
        if (data.type === 'tab' && data.grades) {
            let gradesHtml = '';
            data.grades.forEach((group, index) => {
                let listHtml = '';
                group.items.forEach(item => {
                    let descHtml = applyTooltips(item.desc);
                    listHtml += `
                        <li>
                            <div class="dis-desc">${descHtml}</div>
                            <div class="dis-rate" style="font-weight:700; color:#dc2626;">${item.rate}</div>
                        </li>
                    `;
                });
                gradesHtml += `
                    <div class="accordion-item" id="acc-${index}">
                        <div class="accordion-header" onclick="toggleAccordion(${index})">
                            ${group.category}
                            <span class="material-icons-round">expand_more</span>
                        </div>
                        <div class="accordion-body">
                            <ul class="disability-list">
                                ${listHtml}
                            </ul>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = gradesHtml;
        }

        // 2. 부위별 렌더링
"""

# Let's use regex to replace the old tab logic entirely up to `// 2. 부위별 렌더링`
import re
# We need to replace from `} else if (data.type === 'tab') {` down to `// 2. 부위별 렌더링` (inclusive)
pattern1 = r'\} else if \(data\.type === \'tab\'\) \{[\s\S]*?(?=\s*// 2\.)'
script_text = re.sub(pattern1, new_logic.strip(), script_text, count=1)

# Now in `switchDtTab` we need to handle if grades is clicked when it's hidden, though the button is hidden so it's fine.
codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated loadDisabilityTable for parts_only")
