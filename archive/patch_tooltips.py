import codecs
import re
import json

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

v9807_tooltips = {
    "귓바퀴의 대부분이 결손된 때": { "expId": "exp-4", "tooltip": "귓바퀴의 연골부의 1/2이상 결손된 경우" },
    "14개 이상의 결손": { "expId": "exp-5", "tooltip": "치아의 상실 또는 신경 1/3이상 파절" },
    "7개 이상의 결손": { "expId": "exp-5", "tooltip": "치아의 상실 또는 신경 1/3이상 파절" },
    "5개 이상의 결손": { "expId": "exp-5", "tooltip": "치아의 상실 또는 신경 1/3이상 파절" },
    "뚜렷한 추상": { "expId": "exp-6", "tooltip": "성형수술 후에도 영구히 남는 상태" },
    "외모에 추상": { "expId": "exp-7", "tooltip": "손바닥 1/4 크기 이상 반흔 등" },
    "고도의 기형": { "expId": "exp-8", "tooltip": "35°이상 전만 또는 20°이상 측만변형" },
    "중등도의 기형": { "expId": "exp-8", "tooltip": "15°이상 전만 또는 10°이상 측만변형" },
    "경도의 기형": { "expId": "exp-8", "tooltip": "경도의 전만증 또는 측만변형" },
    "고도의 운동장해": { "expId": "exp-8", "tooltip": "운동범위가 정상범위의 1/4이하로 제한" },
    "중등도의 운동장해": { "expId": "exp-8", "tooltip": "운동범위가 정상범위의 1/2이하로 제한" },
    "경도의 운동장해": { "expId": "exp-8", "tooltip": "운동범위가 정상범위의 3/4 이하로 제한" },
    "고도의 추간반탈출증": { "expId": "exp-8", "tooltip": "추간반을 2마디 이상 수술 등" },
    "중등도의 추간반탈출증": { "expId": "exp-8", "tooltip": "추간반을 1마디 수술로 신경증상 뚜렷" },
    "경도의 추간반탈출증": { "expId": "exp-8", "tooltip": "하지방사통 또는 감각 이상" },
    "고도의 장해": { "expId": "exp-9", "tooltip": "관절운동범위 1/4 이하 제한 등" },
    "중등도의 장해": { "expId": "exp-9", "tooltip": "관절운동범위 1/2 이하 제한 등" },
    "경도의 장해": { "expId": "exp-9", "tooltip": "관절운동범위 3/4 이하 제한 등" },
    "손가락뼈의 일부": { "expId": "exp-10", "tooltip": "심장에 가까운 쪽에서 뼈를 잃은 경우" },
    "발가락뼈의 일부": { "expId": "exp-10", "tooltip": "심장에 가까운 쪽에서 뼈를 잃은 경우" },
    "뚜렷한 장애를 남긴 때": { "expId": "exp-11", "tooltip": "선단에서 뼈를 잃거나 운동범위 1/2 이하" },
    "극심한 장해": { "expId": "exp-12", "tooltip": "기본동작을 전적으로 타인에 의존" },
    "심한 장해": { "expId": "exp-12", "tooltip": "단시간 침상을 떠나는 것이 가능" },
    "기본동작에 제한": { "expId": "exp-12", "tooltip": "이동시 타인의 돌봄이나 보조수단 필요" }
}

v9807_tooltips_json = json.dumps(v9807_tooltips, ensure_ascii=False, indent=4)

# We need to insert `const tooltipKeywords_v9807 = { ... };` below `tooltipKeywords`.
if 'const tooltipKeywords_v9807' not in script_text:
    script_text = script_text.replace(
        'const tooltipKeywords = {', 
        f'const tooltipKeywords_v9807 = {v9807_tooltips_json};\n\nconst tooltipKeywords = {{'
    )

# Update applyTooltips
new_apply_tooltips = """function applyTooltips(text, versionId) {
    let result = text;
    let currentKeywords = tooltipKeywords;
    if (versionId === 'v9807_nonlife') {
        currentKeywords = tooltipKeywords_v9807;
    }
    
    for (const [keyword, info] of Object.entries(currentKeywords)) {
        if (result.includes(keyword)) {
            // Replace only the first occurrence to avoid nested issues
            const html = `<span class="keyword-link" onclick="jumpToExp('${info.expId}')">${keyword}<span class="keyword-tooltip">${info.tooltip}<br><span style="color:#94a3b8; font-size:11px; margin-top:4px; display:block;">클릭하여 상세 해설</span></span></span>`;
            result = result.replace(keyword, html);
        }
    }
    return result;
}"""

script_text = re.sub(r'function applyTooltips\(text\)\s*\{[\s\S]*?return result;\n\}', new_apply_tooltips, script_text)

# Update loadDisabilityTable to pass versionId
script_text = script_text.replace('applyTooltips(item.desc);', 'applyTooltips(item.desc, versionId);')

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Updated tooltips functionality for v9807_nonlife!")
