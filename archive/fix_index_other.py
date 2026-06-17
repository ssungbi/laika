import re

html_path = r"C:\Users\SB\Desktop\연습용\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

view_html = """
            <!-- 7. 등급별 장해표(기타) View -->
            <div id="view-other-disability" class="page-view">
                <div class="content-wrapper">
                    <!-- Title & Back -->
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;">
                        <h2 style="font-size: 24px; font-weight: 700; color: #1e293b; margin: 0; display: flex; align-items: center; gap: 8px;">
                            <span class="material-icons-round" style="color: #6366f1;">format_list_numbered</span>
                            등급별 장해표(기타)
                        </h2>
                        <button class="back-btn" onclick="navigateTo('view-main')" style="background: none; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 16px; font-size: 14px; font-weight: 600; color: #475569; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.2s;">
                            <span class="material-icons-round" style="font-size: 18px;">arrow_back</span>
                            뒤로가기
                        </button>
                    </div>
                    
                    <!-- Major Tabs -->
                    <div class="other-disability-major-tabs" style="display: flex; gap: 10px; margin-bottom: 24px; max-width: 1200px; margin-left: auto; margin-right: auto; justify-content: center; background-color: #f8fafc; padding: 8px; border-radius: 12px; border: 1px solid #e2e8f0;">
                        <button class="major-tab-btn active" data-major="산재" onclick="setOtherDisabilityMajor('산재')" style="flex: 1; padding: 12px 16px; border-radius: 8px; border: none; font-size: 16px; font-weight: 700; cursor: pointer; background-color: #3b82f6; color: white; transition: all 0.2s;">산업재해 장해</button>
                        <button class="major-tab-btn" data-major="자보" onclick="setOtherDisabilityMajor('자보')" style="flex: 1; padding: 12px 16px; border-radius: 8px; border: none; font-size: 16px; font-weight: 700; cursor: pointer; background-color: transparent; color: #64748b; transition: all 0.2s;">자동차손해배상 장해</button>
                        <button class="major-tab-btn" data-major="국배" onclick="setOtherDisabilityMajor('국배')" style="flex: 1; padding: 12px 16px; border-radius: 8px; border: none; font-size: 16px; font-weight: 700; cursor: pointer; background-color: transparent; color: #64748b; transition: all 0.2s;">국가배상 장해</button>
                    </div>

                    <!-- Search -->
                    <div class="insurance-search-container" style="max-width: 1200px; margin: 0 auto 24px auto; position: relative;">
                        <input type="text" id="other-disability-search" placeholder="검색어를 입력하세요..." style="width: 100%; padding: 16px 48px 16px 20px; font-size: 16px; border: 2px solid #e2e8f0; border-radius: 16px; outline: none; transition: all 0.2s; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                        <span class="material-icons-round" style="position: absolute; right: 20px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 24px; pointer-events: none;">search</span>
                    </div>

                    <!-- Sub Tabs -->
                    <div class="other-disability-sub-tabs" style="display: flex; gap: 10px; margin-bottom: 24px; max-width: 1200px; margin-left: auto; margin-right: auto; justify-content: center;">
                        <button class="sub-tab-btn active" data-sub="급수별" onclick="setOtherDisabilitySub('급수별')" style="padding: 10px 24px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 15px; font-weight: 600; cursor: pointer; background-color: #f1f5f9; color: #1e293b; transition: all 0.2s;">급수별</button>
                        <button class="sub-tab-btn" data-sub="부위별" onclick="setOtherDisabilitySub('부위별')" style="padding: 10px 24px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 15px; font-weight: 600; cursor: pointer; background-color: white; color: #64748b; transition: all 0.2s;">부위별</button>
                    </div>

                    <!-- Accordion Area -->
                    <div id="other-disability-content" class="accordion-group" style="max-width: 1200px; margin: 0 auto;">
                        <!-- Content rendered by JS -->
                    </div>
                </div>
            </div>
"""

scripts_html = """
    <script src="other_disability_data.js"></script>
    <script src="other_disability.js"></script>
"""

if "id=\"view-other-disability\"" not in content:
    content = content.replace("</main>", view_html + "\n        </main>")

if "other_disability_data.js" not in content:
    content = content.replace("</body>", scripts_html + "\n</body>")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Injected view and scripts.")
