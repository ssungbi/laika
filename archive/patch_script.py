import codecs

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8').read()

# 1. Inject jumpToExp and applyTooltips functions
js_funcs = """
// 툴팁 키워드 정의
const tooltipKeywords = {
    "항상 간호": { expId: "exp3", tooltip: "이동동작 제한을 포함하고 2개 이상이 제한되거나 수발에 의존" },
    "수시 간호": { expId: "exp4", tooltip: "이동동작 제한을 포함하고 1개 이상 제한, 또는 수시로 타인 수발 필요" },
    "완전 영구히 잃었을 때": { expId: "exp21", tooltip: "장래에 더 이상 호전을 기대할 수 없는 상태" },
    "영구히 남겼을 때": { expId: "exp21", tooltip: "장래에 더 이상 호전을 기대할 수 없는 상태" },
    "추간판탈출증": { expId: "exp19", tooltip: "고도/중도/경도로 분류. 임상증상과 특수검사 소견 일치 시 인정" },
    "일상생활 기본동작": { expId: "exp2", tooltip: "이동, 음식물 섭취, 옷 입고 벗기, 배변, 목욕 동작" },
    "시력을 잃었을": { expId: "exp5", tooltip: "한 눈의 교정시력이 0.02 이하로 되어 회복 불가능" },
    "씹어먹는 기능": { expId: "exp7", tooltip: "물이나 유동식 이외에는 섭취할 수 없는 상태" },
    "관절을 완전 영구히 사용하지 못하게": { expId: "exp12", tooltip: "운동 기능을 완전히 잃거나 완전 강직으로 회복 불가" },
    "관절의 기능에 뚜렷한 장해": { expId: "exp13", tooltip: "주운동방향이 1/2 이하로 제한되거나 동요관절이 있는 경우" },
    "추상": { expId: "exp17", tooltip: "성형수술을 하여도 더 이상 반흔이나 함몰이 없어지지 않는 상태" }
};

function applyTooltips(text) {
    let result = text;
    for (const [keyword, info] of Object.entries(tooltipKeywords)) {
        if (result.includes(keyword)) {
            // Replace only the first occurrence to avoid nested issues
            const html = `<span class="keyword-link" onclick="jumpToExp('${info.expId}')">${keyword}<span class="keyword-tooltip">${info.tooltip}<br><span style="color:#94a3b8; font-size:11px; margin-top:4px; display:block;">클릭하여 자세히 보기</span></span></span>`;
            result = result.replace(keyword, html);
        }
    }
    return result;
}

function jumpToExp(expId) {
    // 1. 해설 탭으로 스위칭
    switchDtTab('explanations');
    
    // 2. 해당 해설 요소 찾기
    const el = document.getElementById(expId);
    if (el) {
        // 약간의 지연 후 스크롤 및 하이라이트 (탭 전환 시간을 벌기 위함)
        setTimeout(() => {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            el.classList.add('exp-highlight');
            // 애니메이션이 끝나면 클래스 제거 (2초 후)
            setTimeout(() => {
                el.classList.remove('exp-highlight');
            }, 2000);
        }, 100);
    }
}
"""

if "applyTooltips(text)" not in script:
    script += "\n" + js_funcs

# 2. Modify loadDisabilityTable to apply applyTooltips and add id to exp-card
# Find the rendering loop for grades
grade_loop_old = "let listHtml = '';\n            group.items.forEach(item => {\n                listHtml += `\n                    <li>\n                        <div class=\"dis-desc\">${item.desc}</div>"
grade_loop_new = "let listHtml = '';\n            group.items.forEach(item => {\n                let descHtml = applyTooltips(item.desc);\n                listHtml += `\n                    <li>\n                        <div class=\"dis-desc\">${descHtml}</div>"

if grade_loop_old in script:
    script = script.replace(grade_loop_old, grade_loop_new)

# Find the rendering loop for parts
part_loop_old = "let pListHtml = '';\n                part.items.forEach(item => {\n                    pListHtml += `\n                        <li>\n                            <div class=\"dis-desc\">${item.desc}</div>"
part_loop_new = "let pListHtml = '';\n                part.items.forEach(item => {\n                    let descHtml = applyTooltips(item.desc);\n                    pListHtml += `\n                        <li>\n                            <div class=\"dis-desc\">${descHtml}</div>"

if part_loop_old in script:
    script = script.replace(part_loop_old, part_loop_new)

# Modify exp-card to include id
exp_old = "<div class=\"exp-card\">\n                    <div class=\"exp-title\">${exp.title}</div>"
exp_new = "<div class=\"exp-card\" id=\"${exp.id || 'exp_idx_'+Math.random().toString(36).substr(2,9)}\">\n                    <div class=\"exp-title\">${exp.title}</div>"

if exp_old in script:
    script = script.replace(exp_old, exp_new)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8').write(script)
print("Applied tooltips to script.js!")
