import re

with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('// Render case tabs if multiple cases exist')
end_idx = text.find('// Default to case 0')

new_code = """// Render case tabs if multiple cases exist
    const casesContainer = document.getElementById('acc-cases-container');
    const casesDescContainer = document.getElementById('acc-cases-desc-container');
    const baseRatioLabel = document.getElementById('acc-base-ratio-label');
    
    if (detail.cases && detail.cases.length > 1) {
        casesContainer.style.display = 'flex';
        casesContainer.innerHTML = '';
        detail.cases.forEach((c, idx) => {
            const isSelected = idx === 0;
            const bg = isSelected ? '#fff' : '#f8fafc';
            const color = isSelected ? '#ef4444' : '#64748b';
            const border = isSelected ? 'border-top: 3px solid #ef4444; border-bottom: none;' : 'border-top: 3px solid transparent; border-bottom: 1px solid #e2e8f0;';
            casesContainer.innerHTML += `
                <button id="acc-case-tab-${idx}" onclick="switchAccidentCase(${idx})" style="padding: 12px 24px; font-weight: bold; font-size: 15px; cursor: pointer; border: none; border-right: 1px solid #e2e8f0; background: ${bg}; color: ${color}; ${border}">
                    ${c.label || '케이스 ' + (idx + 1)}
                </button>
            `;
        });
        
        // Render comparison table
        casesDescContainer.style.display = 'block';
        let tableHtml = `<table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; border: 1px solid #e2e8f0;">`;
        tableHtml += `<tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0;"><th style="padding: 8px; border-right: 1px solid #e2e8f0; text-align: center; width: 60px;">구분</th><th style="padding: 8px; border-right: 1px solid #e2e8f0;">자동차 A</th><th style="padding: 8px;">자동차 B</th></tr>`;
        detail.cases.forEach((c, idx) => {
            tableHtml += `<tr style="border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 8px; border-right: 1px solid #e2e8f0; font-weight: bold; background: #f8fafc; text-align: center;">${c.label || '케이스 ' + (idx+1)}</td>
                <td style="padding: 8px; border-right: 1px solid #e2e8f0;">${c.car_a_text || ''}</td>
                <td style="padding: 8px;">${c.car_b_text || ''}</td>
            </tr>`;
        });
        tableHtml += `</table>`;
        casesDescContainer.innerHTML = tableHtml;
        
        baseRatioLabel.innerText = '기본과실';
    } else {
        casesContainer.style.display = 'none';
        if (casesDescContainer) casesDescContainer.style.display = 'none';
        baseRatioLabel.innerText = '기본과실';
    }

    """

new_text = text[:start_idx] + new_code + text[end_idx:]

with open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("script.js updated successfully.")
