import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the accidental corruption from previous multi_replace
if '"coef_9": "24.0"\n"coef_9": "24.0"' in content:
    content = content.replace('"coef_9": "24.0"\n"coef_9": "24.0"', '"coef_9": "24.0"')

target_start = content.find('<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 40px;">')
if target_start == -1:
    print("Could not find target start")
    sys.exit(1)

target_end = content.find('</div>', target_start + 100) + 6
target_end = content.find('</div>', target_end) + 6

if target_end == 5:
    print("Could not find target end")
    sys.exit(1)

target_block = content[target_start:target_end]

new_block = """<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 40px;">
                <button class="tool-card-new tc-blue" onclick="drillDownAccident('tree1', '자동차와 자동차의 사고')" style="position: relative; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #fff; cursor: pointer; height: 200px; overflow: hidden; transition: all 0.2s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: url('assets/car_vs_car.png'); background-size: cover; background-position: center; opacity: 0.25; z-index: 1;"></div>
                    <div style="position: relative; z-index: 2; font-size: 22px; font-weight: bold; color: #0f172a; text-shadow: 0 2px 4px rgba(255,255,255,0.9), 0 0 10px rgba(255,255,255,0.8);">자동차와 자동차의 사고</div>
                    <div style="position: relative; z-index: 2; font-size: 15px; color: #334155; margin-top: 8px; font-weight: bold; background: rgba(255,255,255,0.7); padding: 4px 12px; border-radius: 12px;">(이륜차 포함)</div>
                </button>
                <button class="tool-card-new tc-green" style="position: relative; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #fff; cursor: not-allowed; height: 200px; overflow: hidden; opacity: 0.8;">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: url('assets/car_vs_pedestrian.png'); background-size: cover; background-position: center; opacity: 0.25; z-index: 1;"></div>
                    <div style="position: relative; z-index: 2; font-size: 22px; font-weight: bold; color: #0f172a; text-shadow: 0 2px 4px rgba(255,255,255,0.9), 0 0 10px rgba(255,255,255,0.8);">자동차와 보행자의 사고</div>
                    <div style="position: relative; z-index: 2; font-size: 15px; color: #334155; margin-top: 8px; font-weight: bold; background: rgba(255,255,255,0.7); padding: 4px 12px; border-radius: 12px;">(준비중)</div>
                </button>
                <button class="tool-card-new tc-purple" style="position: relative; display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #fff; cursor: not-allowed; height: 200px; overflow: hidden; opacity: 0.8;">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: url('assets/car_vs_bicycle.png'); background-size: cover; background-position: center; opacity: 0.25; z-index: 1;"></div>
                    <div style="position: relative; z-index: 2; font-size: 22px; font-weight: bold; color: #0f172a; text-shadow: 0 2px 4px rgba(255,255,255,0.9), 0 0 10px rgba(255,255,255,0.8);">자동차와 자전거의 사고</div>
                    <div style="position: relative; z-index: 2; font-size: 15px; color: #334155; margin-top: 8px; font-weight: bold; background: rgba(255,255,255,0.7); padding: 4px 12px; border-radius: 12px;">(준비중)</div>
                </button>
            </div>"""

content = content.replace(target_block, new_block)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully replaced button HTML in script.js")
