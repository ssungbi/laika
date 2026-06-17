import sys

js_path = r'c:\Users\SB\Desktop\연습용\script.js'
with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """            </div>
                </button>
                <button class="tool-card-new tc-green" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; cursor: not-allowed; height: 200px; opacity: 0.7;">
                    <img src="assets/car_vs_pedestrian.png" style="max-height: 80px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);" alt="차대사람">
                    <div style="font-size: 20px; font-weight: bold; color: #64748b;">자동차와 보행자의 사고</div>
                    <div style="font-size: 14px; color: #94a3b8; margin-top: 8px;">(준비중)</div>
                </button>
                <button class="tool-card-new tc-purple" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; border: 1px solid #cbd5e1; border-radius: 12px; background: #f8fafc; cursor: not-allowed; height: 200px; opacity: 0.7;">
                    <img src="assets/car_vs_bicycle.png" style="max-height: 80px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);" alt="차대자전거">
                    <div style="font-size: 20px; font-weight: bold; color: #64748b;">자동차와 자전거의 사고</div>
                    <div style="font-size: 14px; color: #94a3b8; margin-top: 8px;">(준비중)</div>
                </button>
            </div>
        `;"""

new_target = """            </div>
        `;"""

if target in content:
    content = content.replace(target, new_target)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed leftover buttons in script.js")
else:
    print("Target not found. Let's try regex or manual find.")
