import json
import codecs
import re

# Load v0505_data.json
data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/v0505_data.json', 'r', 'utf-8'))

adl_html = """
<table class="doc-table adls-table" style="width:100%; border-collapse: collapse; margin-top:20px; font-size:14px; border:1px solid #ccc; text-align:center;">
    <thead>
        <tr style="background-color:#f5f5f5; font-weight:bold;">
            <td style="border: 1px solid #ccc; padding: 10px; width:15%;">유형</td>
            <td style="border: 1px solid #ccc; padding: 10px; width:75%;">제한정도</td>
            <td style="border: 1px solid #ccc; padding: 10px; width:10%;">지급률</td>
        </tr>
    </thead>
    <tbody>
        <!-- 이동동작 -->
        <tr>
            <td rowspan="4" style="border: 1px solid #ccc; padding: 8px; font-weight:bold; background-color:#fafafa;">이동동작</td>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 특별한 보조기구를 사용함에도 불구하고 다른 사람의 계속적인 도움이 없이는 방 밖을 나올 수 없는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">40%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 휠체어 또는 다른 사람의 도움 없이는 방 밖을 나올 수 없는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">30%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 목발 또는 보행기(walker)를 사용하지 않으면 독립적인 보행이 불가능한 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">20%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 독립적인 보행은 가능하나 파행이 있는(절뚝거리는) 상태, 난간을 잡지 않고는 계단을 오르내리기가 불가능한 상태, 계속하여 평지에서 100m 이상을 걷지 못하는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">10%</td>
        </tr>
        <!-- 음식물 섭취 -->
        <tr>
            <td rowspan="4" style="border: 1px solid #ccc; padding: 8px; font-weight:bold; background-color:#fafafa;">음식물<br>섭취</td>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 식사를 전혀 할 수 없어 계속적으로 튜브나 경정맥 수액을 통해 부분 혹은 전적인 영양공급을 받는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">20%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 수저 사용이 불가능하여 다른 사람의 계속적인 도움이 없이는 식사를 전혀 할 수 없는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">15%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 숟가락 사용은 가능하나 젓가락 사용이 불가능하여 음식물 섭취에 있어 부분적으로 다른 사람의 도움이 필요한 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">10%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 독립적인 음식물 섭취는 가능하나 젓가락을 이용하여 생선을 바르거나 음식물을 자르지는 못하는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">5%</td>
        </tr>
        <!-- 배변·배뇨 -->
        <tr>
            <td rowspan="4" style="border: 1px solid #ccc; padding: 8px; font-weight:bold; background-color:#fafafa;">배변·<br>배뇨</td>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 배설을 돕기 위해 설치한 의료장치나 외과적 시술물을 사용함에 있어 타인의 계속적인 도움이 필요한 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">20%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 화장실에 가서 변기 위에 앉는 일(요강을 사용하는 일 포함)과 대소변 후에 화장지로 닦고 옷을 입는 일에 다른 사람의 계속적인 도움이 필요한 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">15%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 배변, 배뇨는 독립적으로 가능하나 대소변 후 뒤처리에 있어 다른 사람의 도움이 필요한 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">10%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 빈번하고 불규칙한 배변으로 인해 2시간 이상 계속되는 업무(운전, 작업, 교육 등)를 수행하는 것이 어려운 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">5%</td>
        </tr>
        <!-- 목욕 -->
        <tr>
            <td rowspan="3" style="border: 1px solid #ccc; padding: 8px; font-weight:bold; background-color:#fafafa;">목욕</td>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 다른 사람의 계속적인 도움 없이는 샤워 또는 목욕을 할 수 없는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">10%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 샤워는 가능하나, 혼자서는 때밀기를 할 수 없는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">5%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 목욕시 신체(등 제외)의 일부 부위만 때를 밀 수 있는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">3%</td>
        </tr>
        <!-- 옷입고벗기 -->
        <tr>
            <td rowspan="3" style="border: 1px solid #ccc; padding: 8px; font-weight:bold; background-color:#fafafa;">옷입고벗기</td>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 다른 사람의 계속적인 도움 없이는 전혀 옷을 챙겨 입을 수 없는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">10%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 다른 사람의 계속적인 도움 없이는 상의 또는 하의 중 하나만을 착용할 수 있는 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">5%</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ccc; padding: 8px; text-align:left;">- 착용은 가능하나 다른 사람의 도움 없이는 마무리(단추 잠그고 풀기, 지퍼 올리고 내리기, 끈 묶고 풀기 등)는 불가능한 상태</td>
            <td style="border: 1px solid #ccc; padding: 8px;">3%</td>
        </tr>
    </tbody>
</table>
"""

adl_idx = None
for i, p in enumerate(data['explanations']):
    if 'ADL' in p['title'] or '일상생활' in p['title']:
        p['content'] = adl_html
        adl_idx = i

if adl_idx is not None:
    target_exp_id = f"exp-{adl_idx}"
    for part in data['parts']:
        if '13.' in part['category']:
            for item in part['items']:
                if '일상생활 기본동작' in item['desc']:
                    item['desc'] = item['desc'].replace(
                        '일상생활 기본동작', 
                        f'<a href="#" class="adl-jump-link" style="color:#0056b3; text-decoration:underline; font-weight:bold;" onclick="event.preventDefault(); jumpToExp(\'{target_exp_id}\'); return false;">일상생활 기본동작</a>'
                    )

# Save to v0505_data_adls.json
with codecs.open('c:/Users/SB/Desktop/연습용/v0505_data_adls.json', 'w', 'utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    
print("v0505 ADLs table and link generated.")
