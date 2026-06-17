import re

html_path = r"C:\Users\SB\Desktop\연습용\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

old_header = """                    <!-- Title & Back -->
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;">
                        <h2 style="font-size: 24px; font-weight: 700; color: #1e293b; margin: 0; display: flex; align-items: center; gap: 8px;">
                            <span class="material-icons-round" style="color: #6366f1;">format_list_numbered</span>
                            등급별 장해표(기타)
                        </h2>
                        <button class="back-btn" onclick="navigateTo('view-main')" style="background: none; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 16px; font-size: 14px; font-weight: 600; color: #475569; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.2s;">
                            <span class="material-icons-round" style="font-size: 18px;">arrow_back</span>
                            뒤로가기
                        </button>
                    </div>"""

new_header = """                    <!-- Title & Back -->
                    <div style="display: flex; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; padding-top: 10px;">
                        <button class="back-btn" onclick="navigateTo('view-main')" style="background: none; border: none; cursor: pointer; display: flex; align-items: center; padding: 0; margin-right: 16px; color: #475569; transition: color 0.2s;">
                            <span class="material-icons-round" style="font-size: 28px;">arrow_back</span>
                        </button>
                        <h2 style="font-size: 24px; font-weight: 700; color: #1e293b; margin: 0;">
                            등급별 장해표(기타)
                        </h2>
                    </div>"""

content = content.replace(old_header, new_header)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated header successfully.")
