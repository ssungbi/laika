import codecs

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

old_init = """    // 타이틀 업데이트
    titleEl.textContent = `장해분류표 - ${title}`;
    
    const data = allDisabilityData[versionId];
    
    if (!data || (Array.isArray(data) && data.length === 0)) {"""

new_init = """    // 타이틀 업데이트
    titleEl.textContent = `장해분류표 - ${title}`;
    
    const data = allDisabilityData[versionId];
    
    // Clear all containers
    const partsGroup = document.getElementById('disability-parts');
    const chongchik = document.getElementById('disability-chongchik');
    const criteria = document.getElementById('disability-criteria');
    if(partsGroup) partsGroup.classList.add('hidden');
    if(chongchik) chongchik.classList.add('hidden');
    if(criteria) criteria.classList.add('hidden');
    
    if (!data || (Array.isArray(data) && data.length === 0)) {"""

script_text = script_text.replace(old_init, new_init)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("script.js patched for hiding containers.")
