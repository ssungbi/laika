import codecs

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# I need to update loadDisabilityTable to handle data.type === 'parts_and_exp' logic 
# and introduce data.type === 'v0505_tabs' handling!
# Wait, currently `v0505_unified` has `type: "parts_and_exp"`. I should update it to `type: "v0505_tabs"` first.
script_text = script_text.replace('"type": "parts_and_exp",\n        "grades": [],\n        "parts": [\n            {\n                "category": "1. 눈의 장해",', '"type": "v0505_tabs",\n        "grades": [],\n        "parts": [\n            {\n                "category": "1. 눈의 장해",')


# Now, in loadDisabilityTable, there is the rendering logic.
# I need to find where tabs are handled and inject the v0505_tabs logic.

old_tab_logic = """    } else if (data.type === 'tab' || data.type === 'parts_only' || data.type === 'parts_and_exp') {
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
                tabBtns[0].classList.add('active');
                tabBtns[1].classList.remove('hidden');
                tabBtns[1].classList.remove('active');
                tabBtns[2].classList.remove('hidden');
                tabBtns[2].classList.remove('active');
            }
        }"""

new_tab_logic = """    } else if (data.type === 'tab' || data.type === 'parts_only' || data.type === 'parts_and_exp' || data.type === 'v0505_tabs') {
        const partsContainer = document.getElementById('disability-parts');
        
        if (data.type === 'parts_only') {
            tabs.classList.add('hidden'); // Hide the entire tab bar
        } else if (data.type === 'v0505_tabs') {
            tabs.classList.remove('hidden');
            tabs.innerHTML = `
                <button class="dt-tab active" onclick="switchDtTab('v0505_parts', this)">장해분류표(장해의 분류 + 일상생활 기본동작(ADLs))</button>
                <button class="dt-tab" onclick="switchDtTab('v0505_chongchik', this)">총칙</button>
                <button class="dt-tab" onclick="switchDtTab('v0505_criteria', this)">장해판정기준</button>
            `;
        } else {
            tabs.classList.remove('hidden');
            // reset to original tabs if it was changed
            tabs.innerHTML = `
                <button class="dt-tab active" onclick="switchDtTab('grades', this)">장해 등급표</button>
                <button class="dt-tab" onclick="switchDtTab('parts', this)">부위별 장해등급표</button>
                <button class="dt-tab" onclick="switchDtTab('explanations', this)">장해 해설 및 평가기준</button>
            `;
            const tabBtns = document.querySelectorAll('#dt-tabs .dt-tab');
            if (data.type === 'parts_and_exp') {
                tabBtns[0].classList.add('hidden'); // Hide Grades tab
                tabBtns[1].classList.remove('hidden');
                tabBtns[1].classList.add('active'); // Activate Parts tab
                tabBtns[2].classList.remove('hidden');
                tabBtns[2].classList.remove('active');
            } else {
                tabBtns[0].classList.remove('hidden');
                tabBtns[0].classList.add('active');
                tabBtns[1].classList.remove('hidden');
                tabBtns[1].classList.remove('active');
                tabBtns[2].classList.remove('hidden');
                tabBtns[2].classList.remove('active');
            }
        }"""
        
script_text = script_text.replace(old_tab_logic, new_tab_logic)


# Now, populating the parts, chongchik and criteria containers for v0505_tabs

old_render_logic = """        // Parts rendering
        if (data.parts && data.parts.length > 0) {
            let partsBoxHtml = '';
            data.parts.forEach(part => {
                let itemsHtml = part.items.map(item => `
                    <tr>
                        <td>${applyTooltips(item.desc, versionId)}</td>
                        <td class="text-center">${item.rate}</td>
                    </tr>
                `).join('');
                
                // --- Here we render bottom explanation box for v9807_nonlife (and potentially v0505_unified initially) ---
                let expBoxHtml = '';
                if ((versionId === 'v9807_nonlife' || versionId === 'v0505_unified') && part.expIndices && data.explanations) {
                    expBoxHtml = '<div class="part-exp-box"><div class="part-exp-title">관련 장해 해설</div>';
                    part.expIndices.forEach(eIdx => {
                        const expData = data.explanations[eIdx];
                        if (expData) {
                            expBoxHtml += `
                                <div class="part-exp-item">
                                    <div class="part-exp-item-title">${expData.title}</div>
                                    <div class="part-exp-item-content">${expData.content.replace(/\\n/g, '<br>')}</div>
                                </div>
                            `;
                        }
                    });
                    expBoxHtml += '</div>';
                }

                partsBoxHtml += `
                    <div class="accordion-item">
                        <button class="accordion-header" onclick="this.classList.toggle('active'); this.nextElementSibling.classList.toggle('active')">
                            ${part.category}
                            <span class="material-icons-round expand-icon">expand_more</span>
                        </button>
                        <div class="accordion-content">
                            <table class="data-table mt-2">
                                <colgroup>
                                    <col>
                                    <col style="width: 100px">
                                </colgroup>
                                <thead>
                                    <tr>
                                        <th>장해의 종류</th>
                                        <th>지급률(%)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${itemsHtml}
                                </tbody>
                            </table>
                            ${expBoxHtml}
                        </div>
                    </div>
                `;
            });
            partsContainer.innerHTML = partsBoxHtml;
        }"""
        
new_render_logic = """        // Parts rendering
        if (data.parts && data.parts.length > 0) {
            let partsBoxHtml = '';
            data.parts.forEach(part => {
                let itemsHtml = part.items.map(item => `
                    <tr>
                        <td>${applyTooltips(item.desc, versionId)}</td>
                        <td class="text-center">${item.rate}</td>
                    </tr>
                `).join('');
                
                // --- Bottom explanation box (only for v9807_nonlife now, since v0505 has a separate tab) ---
                let expBoxHtml = '';
                if (versionId === 'v9807_nonlife' && part.expIndices && data.explanations) {
                    expBoxHtml = '<div class="part-exp-box"><div class="part-exp-title">관련 장해 해설</div>';
                    part.expIndices.forEach(eIdx => {
                        const expData = data.explanations[eIdx];
                        if (expData) {
                            expBoxHtml += `
                                <div class="part-exp-item">
                                    <div class="part-exp-item-title">${expData.title}</div>
                                    <div class="part-exp-item-content">${expData.content.replace(/\\n/g, '<br>')}</div>
                                </div>
                            `;
                        }
                    });
                    expBoxHtml += '</div>';
                }

                partsBoxHtml += `
                    <div class="accordion-item">
                        <button class="accordion-header" onclick="this.classList.toggle('active'); this.nextElementSibling.classList.toggle('active')">
                            ${part.category}
                            <span class="material-icons-round expand-icon">expand_more</span>
                        </button>
                        <div class="accordion-content">
                            <table class="data-table mt-2">
                                <colgroup>
                                    <col>
                                    <col style="width: 100px">
                                </colgroup>
                                <thead>
                                    <tr>
                                        <th>장해의 종류</th>
                                        <th>지급률(%)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${itemsHtml}
                                </tbody>
                            </table>
                            ${expBoxHtml}
                        </div>
                    </div>
                `;
            });
            
            // If v0505_tabs, append ADLs to partsContainer
            if (data.type === 'v0505_tabs' && data.explanations) {
                // ADLs is index 14
                const adlsData = data.explanations[14];
                if (adlsData) {
                    partsBoxHtml += `
                        <div class="accordion-item mt-4">
                            <button class="accordion-header" onclick="this.classList.toggle('active'); this.nextElementSibling.classList.toggle('active')">
                                ${adlsData.title}
                                <span class="material-icons-round expand-icon">expand_more</span>
                            </button>
                            <div class="accordion-content">
                                <div class="exp-content">${adlsData.content.replace(/\\n/g, '<br>')}</div>
                            </div>
                        </div>
                    `;
                }
            }
            
            partsContainer.innerHTML = partsBoxHtml;
        }"""

script_text = script_text.replace(old_render_logic, new_render_logic)

# Explanations Rendering Update
old_exp_logic = """        // Explanations rendering
        if (data.explanations && data.explanations.length > 0) {
            const expContainer = document.getElementById('disability-explanations');
            let expHtml = data.explanations.map(exp => `
                <div class="exp-item" id="${exp.id || ''}">
                    <h4 class="exp-title">${exp.title}</h4>
                    <div class="exp-content">${exp.content.replace(/\\n/g, '<br>')}</div>
                </div>
            `).join('');
            expContainer.innerHTML = expHtml;
        }"""

new_exp_logic = """        // Explanations rendering
        if (data.explanations && data.explanations.length > 0) {
            if (data.type === 'v0505_tabs') {
                const chongchikContainer = document.getElementById('disability-chongchik');
                const criteriaContainer = document.getElementById('disability-criteria');
                
                // Chongchik (index 0)
                const chongData = data.explanations[0];
                chongchikContainer.innerHTML = `
                    <div class="exp-item">
                        <h4 class="exp-title">${chongData.title}</h4>
                        <div class="exp-content">${chongData.content.replace(/\\n/g, '<br>')}</div>
                    </div>
                `;
                
                // Criteria (index 1 ~ 13)
                let crHtml = '';
                for (let i = 1; i <= 13; i++) {
                    const crData = data.explanations[i];
                    if (crData) {
                        crHtml += `
                            <div class="exp-item">
                                <h4 class="exp-title">${crData.title}</h4>
                                <div class="exp-content">${crData.content.replace(/\\n/g, '<br>')}</div>
                            </div>
                        `;
                    }
                }
                criteriaContainer.innerHTML = crHtml;
                
            } else {
                const expContainer = document.getElementById('disability-explanations');
                let expHtml = data.explanations.map(exp => `
                    <div class="exp-item" id="${exp.id || ''}">
                        <h4 class="exp-title">${exp.title}</h4>
                        <div class="exp-content">${exp.content.replace(/\\n/g, '<br>')}</div>
                    </div>
                `).join('');
                expContainer.innerHTML = expHtml;
            }
        }"""

script_text = script_text.replace(old_exp_logic, new_exp_logic)

# Init switchDtTab
old_init_tab = """    if (data.type === 'tab') {
        switchDtTab('grades');
    } else if (data.type === 'parts_only') {
        switchDtTab('parts');
    } else if (data.type === 'parts_and_exp') {
        switchDtTab('parts');
    }"""
    
new_init_tab = """    if (data.type === 'tab') {
        switchDtTab('grades');
    } else if (data.type === 'parts_only') {
        switchDtTab('parts');
    } else if (data.type === 'parts_and_exp') {
        switchDtTab('parts');
    } else if (data.type === 'v0505_tabs') {
        switchDtTab('v0505_parts');
    }"""

script_text = script_text.replace(old_init_tab, new_init_tab)


codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("script.js rendering logic updated.")
