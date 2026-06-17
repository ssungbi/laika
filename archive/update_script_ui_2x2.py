import re

with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('// Top Level Hardcode if current path is empty')
end_idx = text.find('return;', start_idx) + 7

new_code = """// Top Level Hardcode if current path is empty
    if(currentAccidentPath.length === 0) {
        navContainer.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 40px;">
                <button class="tool-card-new tc-blue" onclick="drillDownAccident('tree1', '자동차 vs 자동차 (고속도로 포함)')" style="position: relative; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #fff; cursor: pointer; height: 200px; overflow: hidden; transition: all 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: url('assets/car_vs_car.png'); background-size: cover; background-position: center; opacity: 0.25; z-index: 1;"></div>
                    <div style="position: relative; z-index: 2; font-size: 22px; font-weight: bold; color: #0f172a; text-shadow: 0 2px 4px rgba(255,255,255,0.9), 0 0 10px rgba(255,255,255,0.8); text-align: center;">자동차 vs 자동차<br><span style="font-size: 16px; font-weight: 500;">(고속도로 포함)</span></div>
                </button>
                <button class="tool-card-new tc-green" onclick="drillDownAccident('tree2', '자동차 vs 보행자')" style="position: relative; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #fff; cursor: pointer; height: 200px; overflow: hidden; transition: all 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: url('assets/car_vs_pedestrian.png'); background-size: cover; background-position: center; opacity: 0.25; z-index: 1;"></div>
                    <div style="position: relative; z-index: 2; font-size: 22px; font-weight: bold; color: #0f172a; text-shadow: 0 2px 4px rgba(255,255,255,0.9), 0 0 10px rgba(255,255,255,0.8);">자동차 vs 보행자</div>
                </button>
                <button class="tool-card-new tc-orange" onclick="drillDownAccident('tree3', '자동차 vs 이륜차')" style="position: relative; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #fff; cursor: pointer; height: 200px; overflow: hidden; transition: all 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: url('assets/car_vs_motorcycle.png'); background-size: cover; background-position: center; opacity: 0.25; z-index: 1; background-color: #fef08a;"></div>
                    <div style="position: relative; z-index: 2; font-size: 22px; font-weight: bold; color: #0f172a; text-shadow: 0 2px 4px rgba(255,255,255,0.9), 0 0 10px rgba(255,255,255,0.8);">자동차 vs 이륜차</div>
                </button>
                <button class="tool-card-new tc-purple" onclick="drillDownAccident('tree4', '자동차 vs 자전거')" style="position: relative; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #fff; cursor: pointer; height: 200px; overflow: hidden; transition: all 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: url('assets/car_vs_bicycle.png'); background-size: cover; background-position: center; opacity: 0.25; z-index: 1;"></div>
                    <div style="position: relative; z-index: 2; font-size: 22px; font-weight: bold; color: #0f172a; text-shadow: 0 2px 4px rgba(255,255,255,0.9), 0 0 10px rgba(255,255,255,0.8);">자동차 vs 자전거</div>
                </button>
            </div>
        `;
        return;
"""

text = text[:start_idx] + new_code + text[end_idx:]

with open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("script.js UI updated to 2x2 layout.")
