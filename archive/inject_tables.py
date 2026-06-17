import json
import re

# Load tables
with open("part2_tables.json", "r", encoding="utf-8") as f:
    tables = json.load(f)

def make_html_table(table_data):
    html = "<div style='overflow-x: auto;'><table style='width:100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; font-size: 13px; text-align: left;'>"
    for r_idx, row in enumerate(table_data):
        html += "<tr>"
        for cell in row:
            val = str(cell) if cell is not None else ""
            val = val.replace("\n", "<br>")
            if r_idx == 0:
                html += f"<th style='border: 1px solid #cbd5e1; padding: 8px; background-color: #f1f5f9; font-weight: bold; white-space: nowrap;'>{val}</th>"
            else:
                html += f"<td style='border: 1px solid #cbd5e1; padding: 8px;'>{val}</td>"
        html += "</tr>"
    html += "</table></div>"
    return html

mapping = [
    (0, "두 부", "세부 상해 급수표 (표)"),
    (1, "두 부", "GCS 운동 반응 점수 (표)"),
    (2, "두 부", "GCS 척도별 상태 (표)"),
    (3, "안과, 이비인후과, 안면부", "안과/이비인후과/안면부 상해 급수표 (표)"),
    (4, "척추", "MMT 근력 등급 (표)"),
    (5, "척추", "척추 상해 급수표 (표)"),
    (6, "흉부, 복부, 비뇨기과", "흉부/복부/비뇨기과 상해 급수표 (표)"),
    (7, "상하지 공통", "절단 상해 급수표 (표)"),
    (8, "상하지 공통", "상지 - 상완/견관절 상해 급수표 (표)"),
    (9, "상하지 공통", "상지 - 상완골 상해 급수표 (표)"),
    (10, "상하지 공통", "상지 - 주관절/요골/척골 상해 급수표 (표)"),
    (11, "상하지 공통", "상지 - 완관절/수근/수지 상해 급수표 (표)"),
    (12, "상하지 공통", "하지 - 고관절/골반/대퇴골 상해 급수표 (표)"),
    (13, "상하지 공통", "하지 - 슬관절/경골/비골 상해 급수표 (표)"),
    (14, "상하지 공통", "하지 - 족관절 상해 급수표 (표)"),
    (15, "상하지 공통", "하지 - 중족골/족지골 상해 급수표 (표)"),
    (16, "상하지 공통", "연부조직 상해 급수표 (표)"),
    (17, "치아", "치아 상해 급수표 (표)")
]

# Build guidelines object
guidelines_dict = {
    "공통사항": [
        {"title": "병급 및 조정 요인", "content": "가. 2급부터 11급까지의 상해 내용중 2가지 이상의 상해가 중복된 경우에는 가장 높은 등급에 해당하는 상해로부터 하위 3등급(예: 상해내용이 주로 2급에 해당하는 경우에는 5급까지)사이의 상해가 중복된 경우에만 가장 높은 상해 내용의 등급보다 한등급 높은 금액으로 배상한다.(이하 \"병급\"이라 한다)\\n나. 일반외상과 치과보철을 필요로 하는 상해가 중복된 경우에는 각각의 상해 등급별 금액을 배상하되 그 합산액이 1급의 금액을 초과하지 아니하는 범위에서 배상한다.\\n다. 1개의 상해에서 2개이상의 상향 또는 하향 조정의 요인이 있을때, 등급 상향 또는 하향조정은 1회만 큰폭의 조정을 적용한다. 다만, 상향 조정 요인과 하향 조정 요인이 여러 개가 함께있을때는 큰폭의 상향 또는 하향 조정 요인을 각각 선택하여 함께 반영한다.\\n※ 골절에 말초신경마비 있는 경우 1급 상향하고, 개방성이면 1급 또 상향하여야 하나 2개의상향요인이므로 한번만 상향하라는 의미임."},
        {"title": "기타 공통", "content": "라. 재해 발생시 만 13세 미만인 사람은 소아로 인정한다.\\n마. 연부조직에 손상이 심하여 유리 피판술, 유경 피판술, 원거리 피판술, 국소 피판술 이나 피부 이식술을 시행할 경우, 안면부는 1등급 상위등급을 적용하고, 수부, 족부에 국한된 손상에 대하여는 한등급 아래의 등급을 적용한다\\n※ 수부, 족부, 손가락, 발가락, 손등, 발등을 말하며 족관절, 완관절 이상은 사지부로 본다"}
    ],
    "두 부": [
        {"title": "자배법 세부 지침", "content": "가. \"뇌손상\"이란 국소성 뇌손상인 외상성 두개강안의 출혈(경막상ㆍ하 출혈, 뇌실 내 및 뇌실질 내 출혈, 거미막하 출혈 등을 말한다) 또는 경막하 수활액낭종, 거미막 낭종, 두개골 골절(두개 기저부 골절을 포함한다) 등과 미만성 축삭손상을 포함한 뇌좌상을 말한다. ※ 수술종류 불문하고 ‘수술을 시행한 경우’ ‘수술을 시행하지 않은 경우’ 구분\\n나. 4급 이하(4급에서 14급까지를 말한다)에서 의식 외에 뇌신경 손상이나 국소성 신경학적 이상 소견이 있는 경우 한 등급을 상향 조정할 수 있다.\\n다. 신경학적 증상은 글라스고우 혼수척도(Glasgow coma scale)로 구분하며, 고도는 8점 이하, 중등도는 9점 이상 12점 이하, 경도는 13점 이상 15점 이하를 말한다.\\n사. 두피 좌상, 열창은 14급으로 본다.\\n아. 만성 경막하 혈종으로 수술을 시행한 경우에는 6급 2호를 적용한다.\\n자. 외상 후 급성 스트레스 장애는 다른 진단이 전혀 없이 단독 상병으로 외상 후 1개월 이내 발병된 경우에 적용한다."}
    ],
    "안과, 이비인후과, 안면부": [
        {"title": "세부 내용 및 참고", "content": "※안와골절로 수술무: 안면두개골골절 8급2항 준용\\n※다발성 안면 두개골 골절(수술여부 불문) 안면두개골:누골,비골,서골,관골,하비갑개,구개골,상악골,하악골, 설골,치조골\\n참고(손보협회 준용): 가. 안구 – 좌,우측 각각 적용\\n나. 10급 3항: 각막 공막 등의 열상으로 일차 봉합술만 시행한 상태 - 수술 미시행 12급 준용 / 안경파손, 인공의안 원상복구 14급 준용"}
    ],
    "척추": [
        {"title": "자배법 세부 지침", "content": "가. 완전 마비는 근력등급 3 이하인 경우이며, 불완전 마비는 근력등급 4인 경우로 정한다.\\n나. 척추관 협착증이나 추간판 탈출증이 외상으로 증상이 발생한 경우나 악화된 경우는 9급으로 본다.\\n다. 척주 손상으로 인하여 신경근증 이나 감각이상을 호소하는 경우는 9급으로 본다.\\n라. 마미증후군은 척수손상으로 본다."}
    ],
    "흉부, 복부, 비뇨기과": [
        {"title": "자배법 세부 지침 및 참고", "content": "심장타박(6급)의 경우\\n① 심전도에서 Tachyarrythmia또는 ST변화 또는 부정맥\\n② 심초음파에서 심낭액 증가 소견이 있거나 심장벽 운동저하\\n③ 심장효소치 증가(CPK-MB, and Troponin T) 세가지 요구 충족시 인정한다\\n참고:\\n장기의 일부라도 적출했다면 2급3항 적용이 타당, 장기의 적출술은 반드시 장기를 모두 떼어내는 전적출술만이 아니라 일부라도 잘라내는 것도 적출술에 해당"}
    ],
    "상하지 공통": [
        {"title": "자배법 세부 지침", "content": "가. 2급부터 11급까지의 내용 중 사지 골절에서 별도로 상해 등급이 규정되지 않은 경우, 보존적 치료를 시행한 골절은 해당 등급에서 2급 낮은 등급을 적용하며, 도수 정복 및 경피적 핀고정술을 시행한 경우에는 해당 등급에서 1급 낮은 등급을 적용한다.\\n나. 2급부터 11급까지의 상해 내용 중 개방성 골절 또는 탈구에서 거스틸로 2형 이상(개방창의 길이가 1cm 이상인 경우를 말한다)의 개방성 골절 또는 탈구에서만 1등급 상위 등급을 적용한다.\\n다. \"수술적 치료를 시행하지 않은\"이라고 명기되지 않은 각 등급 손상 내용은 수술적 치료를 시행한 경우를 말하며, 보존적 치료를 시행한 경우가 따로 명시되지 않은 경우는 두 등급 하향 조정함을 원칙으로 한다.\\n라. 양측 또는 단측을 별도로 규정한 경우에는 병합하지 않으나, 별도 규정이 없는 양측 손상인 경우에는 병합한다.\\n마. 골절에 주요 말초신경의 손상 동반 시 해당 골절보다 1등급 상위 등급을 적용한다.\\n버. 소아의 경우, 성인의 동일 부위 골절보다 1급 낮게 적용한다. 다만, 성장판 손상이 동반된 경우와 연부조직 손상은 성인과 동일한 등급을 적용한다."}
    ],
    "치아": [
        {"title": "세부 지침", "content": "일반 외상과 치과 보철을 필요로 하는 상해가 중복된 경우 각 각의 상해 등급별 금액을 배상하되 그 합산액이 1급의 금액을 초과하지 아니하는 범위에서 배상한다.\\n가. 총의치 국부의치의 원상복귀는 12급에 준용한다.\\n나. 이번 교통사고로 기존 보철물이 파손된 경우에는 치아보철 개수에 따른 치아 급수를 적용한다.\\n다. 임플란트: 시행한 개수로 급항 결정(예: 임플란트 2개 시행 13급 적용)"}
    ]
}

# Append HTML tables
for item in mapping:
    t_idx = item[0]
    cat = item[1]
    title = item[2]
    table_data = tables[t_idx]["table"]
    html_str = make_html_table(table_data)
    
    if cat not in guidelines_dict:
        guidelines_dict[cat] = []
        
    guidelines_dict[cat].append({
        "title": title,
        "content": html_str
    })

# Format to JS string
guidelines_js = "    guidelines: [\n"
for cat, subcats in guidelines_dict.items():
    guidelines_js += "        {\n"
    guidelines_js += f'            category: "{cat}",\n'
    guidelines_js += "            subcategories: [\n"
    for sub in subcats:
        title = sub["title"]
        content = sub["content"].replace('"', '\\"').replace("\n", "")
        guidelines_js += "                {\n"
        guidelines_js += f'                    title: "{title}",\n'
        guidelines_js += f'                    content: "{content}"\n'
        guidelines_js += "                },\n"
    guidelines_js = guidelines_js.rstrip(",\n") + "\n"
    guidelines_js += "            ]\n"
    guidelines_js += "        },\n"
guidelines_js = guidelines_js.rstrip(",\n") + "\n    ]\n"

js_path = r"C:\Users\SB\Desktop\연습용\injury_data.js"
with open(js_path, "r", encoding="utf-8") as f:
    original = f.read()

# Replace the old guidelines block
start_idx = original.find("    // 3. 영역별 세부지침")
if start_idx != -1:
    end_idx = original.find("};", start_idx)
    new_js = original[:start_idx] + "    // 3. 영역별 세부지침\n" + guidelines_js + original[end_idx:]
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(new_js)
    print("Successfully injected tables into injury_data.js")
else:
    print("Could not find guidelines section")
