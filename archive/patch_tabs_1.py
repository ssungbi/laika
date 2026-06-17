import codecs

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# 1. First, modify switchDtTab to handle dynamic tabs gracefully without breaking others.
# Actually, let's just make switchDtTab take the target container ID!
# Wait, it's easier to just add the logic to switchDtTab.
old_switch = """function switchDtTab(tabName) {
    const tabs = document.querySelectorAll('.dt-tab');
    tabs.forEach(t => t.classList.remove('active'));
    
    // 탭 찾아서 활성화
    if (tabName === 'grades') tabs[0].classList.add('active');
    if (tabName === 'parts') tabs[1].classList.add('active');
    if (tabName === 'explanations') tabs[2].classList.add('active');

    const accordion = document.getElementById('disability-accordion');
    const partsGroup = document.getElementById('disability-parts');
    const explanations = document.getElementById('disability-explanations');

    accordion.classList.add('hidden');
    partsGroup.classList.add('hidden');
    explanations.classList.add('hidden');

    if (tabName === 'grades') {
        accordion.classList.remove('hidden');
    } else if (tabName === 'parts') {
        partsGroup.classList.remove('hidden');
    } else {
        explanations.classList.remove('hidden');
    }
}"""

new_switch = """function switchDtTab(tabName, btnElement) {
    // If btnElement is provided (dynamic tabs), use it
    if (btnElement) {
        const tabs = btnElement.parentElement.querySelectorAll('.dt-tab');
        tabs.forEach(t => t.classList.remove('active'));
        btnElement.classList.add('active');
    } else {
        const tabs = document.querySelectorAll('#dt-tabs .dt-tab');
        tabs.forEach(t => t.classList.remove('active'));
        if (tabName === 'grades' && tabs[0]) tabs[0].classList.add('active');
        if (tabName === 'parts' && tabs[1]) tabs[1].classList.add('active');
        if (tabName === 'explanations' && tabs[2]) tabs[2].classList.add('active');
    }

    const accordion = document.getElementById('disability-accordion');
    const partsGroup = document.getElementById('disability-parts');
    const explanations = document.getElementById('disability-explanations');
    
    // For v0505
    const chongchik = document.getElementById('disability-chongchik');
    const criteria = document.getElementById('disability-criteria');

    if(accordion) accordion.classList.add('hidden');
    if(partsGroup) partsGroup.classList.add('hidden');
    if(explanations) explanations.classList.add('hidden');
    if(chongchik) chongchik.classList.add('hidden');
    if(criteria) criteria.classList.add('hidden');

    if (tabName === 'grades') {
        if(accordion) accordion.classList.remove('hidden');
    } else if (tabName === 'parts') {
        if(partsGroup) partsGroup.classList.remove('hidden');
    } else if (tabName === 'explanations') {
        if(explanations) explanations.classList.remove('hidden');
    } else if (tabName === 'v0505_parts') {
        if(partsGroup) partsGroup.classList.remove('hidden');
    } else if (tabName === 'v0505_chongchik') {
        if(chongchik) chongchik.classList.remove('hidden');
    } else if (tabName === 'v0505_criteria') {
        if(criteria) criteria.classList.remove('hidden');
    }
}"""

script_text = script_text.replace(old_switch, new_switch)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("switchDtTab updated.")
