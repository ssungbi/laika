import re

with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('// Render comparison table')
end_idx = text.find('baseRatioLabel.innerText')

new_code = """// Render comparison table
        casesDescContainer.style.display = 'block';
        let tableHtml = `<table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; border: 1px solid #e2e8f0; table-layout: fixed;">`;
        
        // Row 1: Header (사고상황 | (가) | (나))
        tableHtml += `<tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0;">`;
        tableHtml += `<th style="padding: 8px; border-right: 1px solid #e2e8f0; text-align: center; vertical-align: middle; width: 20%;">사고상황</th>`;
        detail.cases.forEach((c, idx) => {
            const isLast = idx === detail.cases.length - 1;
            tableHtml += `<th style="padding: 8px; text-align: center; vertical-align: middle; ${!isLast ? 'border-right: 1px solid #e2e8f0;' : ''}">${c.label || '케이스 ' + (idx+1)}</th>`;
        });
        tableHtml += `</tr>`;
        
        // Row 2: 자동차 A
        tableHtml += `<tr style="border-bottom: 1px solid #e2e8f0;">`;
        tableHtml += `<td style="padding: 8px; border-right: 1px solid #e2e8f0; font-weight: bold; background: #f8fafc; text-align: center; vertical-align: middle;">자동차 A</td>`;
        detail.cases.forEach((c, idx) => {
            const isLast = idx === detail.cases.length - 1;
            tableHtml += `<td style="padding: 8px; vertical-align: middle; ${!isLast ? 'border-right: 1px solid #e2e8f0;' : ''}">${c.car_a_text || ''}</td>`;
        });
        tableHtml += `</tr>`;
        
        // Row 3: 자동차 B
        tableHtml += `<tr>`;
        tableHtml += `<td style="padding: 8px; border-right: 1px solid #e2e8f0; font-weight: bold; background: #f8fafc; text-align: center; vertical-align: middle;">자동차 B</td>`;
        detail.cases.forEach((c, idx) => {
            const isLast = idx === detail.cases.length - 1;
            tableHtml += `<td style="padding: 8px; vertical-align: middle; ${!isLast ? 'border-right: 1px solid #e2e8f0;' : ''}">${c.car_b_text || ''}</td>`;
        });
        tableHtml += `</tr>`;
        
        tableHtml += `</table>`;
        casesDescContainer.innerHTML = tableHtml;
        
        """

new_text = text[:start_idx] + new_code + text[end_idx:]

with open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("script.js table logic updated successfully.")
