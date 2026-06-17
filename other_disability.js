try {
    window.currentOtherDisabilityMajor = "산재";
    window.currentOtherDisabilitySub = "급수별";
    window.otherDisabilitySearchTerm = "";

    // Initialize
    document.addEventListener("DOMContentLoaded", () => {
        const searchInput = document.getElementById("other-disability-search");
        if (searchInput) {
            searchInput.addEventListener("input", (e) => {
                window.otherDisabilitySearchTerm = e.target.value.trim().toLowerCase();
                window.renderOtherDisabilityContent();
            });
        }
    });

    window.setOtherDisabilityMajor = function(major) {
        window.currentOtherDisabilityMajor = major;
        
        document.querySelectorAll(".major-tab-btn").forEach(btn => {
            if (btn.dataset.major === major) {
                btn.classList.add("active");
                btn.style.backgroundColor = "#3b82f6";
                btn.style.color = "white";
            } else {
                btn.classList.remove("active");
                btn.style.backgroundColor = "transparent";
                btn.style.color = "#64748b";
            }
        });

        const searchInput = document.getElementById("other-disability-search");
        if (searchInput) {
            searchInput.value = "";
            window.otherDisabilitySearchTerm = "";
        }

        // 대분류 전환 시 중분류를 항상 "급수별"로 초기화
        window.setOtherDisabilitySub("급수별");
    }

    window.setOtherDisabilitySub = function(sub) {
        window.currentOtherDisabilitySub = sub;
        
        document.querySelectorAll(".other-disability-sub-tabs .sub-tab-btn").forEach(btn => {
            if (btn.dataset.sub === sub) {
                btn.classList.add("active");
                btn.style.backgroundColor = "#f1f5f9";
                btn.style.color = "#1e293b";
            } else {
                btn.classList.remove("active");
                btn.style.backgroundColor = "white";
                btn.style.color = "#64748b";
            }
        });

        window.renderOtherDisabilityContent();
    }

    window.renderOtherDisabilityContent = function() {
        const container = document.getElementById("other-disability-content");
        if (!container) return;

        const majorData = window.otherDisabilityData[window.currentOtherDisabilityMajor];
        if (!majorData) {
            container.innerHTML = "<div style='text-align:center; padding: 40px; color: #64748b;'>데이터를 준비 중입니다.</div>";
            return;
        }

        let html = "";
        const term = window.otherDisabilitySearchTerm;

        if (window.currentOtherDisabilitySub === "급수별") {
            majorData.grades.forEach(gradeObj => {
                const filteredItems = gradeObj.items.filter(item => {
                    if (!term) return true;
                    return gradeObj.grade.toLowerCase().includes(term) ||
                           item.part.toLowerCase().includes(term) ||
                           item.desc.toLowerCase().includes(term);
                });

                if (filteredItems.length === 0 && term) return;

                html += `
                    <div class="accordion-item" style="border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; background: white;">
                        <button class="accordion-header" onclick="this.parentElement.classList.toggle('active')" style="width: 100%; text-align: left; padding: 16px 20px; background: none; border: none; font-size: 16px; font-weight: 700; color: #1e293b; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: background-color 0.2s;">
                            <span>${gradeObj.grade}</span>
                            <span class="material-icons-round icon">expand_more</span>
                        </button>
                        <div class="accordion-content">
                            <ul style="list-style: none; padding: 0; margin: 16px 0 0 0;">
                                ${filteredItems.map(item => `
                                    <li style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px dashed #e2e8f0; display: flex; align-items: flex-start; gap: 12px;">
                                        <span style="display: inline-block; padding: 4px 10px; background-color: #f1f5f9; color: #475569; border-radius: 6px; font-size: 13px; font-weight: 600; white-space: nowrap; flex-shrink: 0;">[${item.part}]</span>
                                        <span style="font-size: 15px; color: #334155; line-height: 1.6; flex: 1;">${window.highlightTextOther(item.desc, term)}</span>
                                    </li>
                                `).join("")}
                            </ul>
                        </div>
                    </div>
                `;
            });
        } else if (window.currentOtherDisabilitySub === "부위별") {
            majorData.parts.forEach(partObj => {
                if (!partObj.items || partObj.items.length === 0) return;
                const filteredItems = partObj.items.filter(item => {
                    if (!term) return true;
                    return partObj.part.toLowerCase().includes(term) ||
                           item.grade.toLowerCase().includes(term) ||
                           item.desc.toLowerCase().includes(term);
                });

                if (filteredItems.length === 0 && term) return;

                html += `
                    <div class="accordion-item" style="border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; background: white;">
                        <button class="accordion-header" onclick="this.parentElement.classList.toggle('active')" style="width: 100%; text-align: left; padding: 16px 20px; background: none; border: none; font-size: 16px; font-weight: 700; color: #1e293b; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: background-color 0.2s;">
                            <span>${partObj.part}</span>
                            <span class="material-icons-round icon">expand_more</span>
                        </button>
                        <div class="accordion-content">
                            <ul style="list-style: none; padding: 0; margin: 16px 0 0 0;">
                                ${filteredItems.map(item => `
                                    <li style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px dashed #e2e8f0; display: flex; align-items: flex-start; gap: 12px;">
                                        <span style="display: inline-block; padding: 4px 10px; background-color: #ef4444; color: white; border-radius: 6px; font-size: 13px; font-weight: 700; white-space: nowrap; flex-shrink: 0;">${item.grade}</span>
                                        <span style="font-size: 15px; color: #334155; line-height: 1.6; flex: 1;">${window.highlightTextOther(item.desc, term)}</span>
                                    </li>
                                `).join("")}
                            </ul>
                        </div>
                    </div>
                `;
            });
        }

        if (!html && term) {
            html = "<div style='text-align:center; padding: 40px; color: #64748b;'>검색 결과가 없습니다.</div>";
        }

        container.innerHTML = html;
        
        if (term) {
            container.querySelectorAll(".accordion-item").forEach(item => {
                item.classList.add("active");
            });
        }
    }

    window.highlightTextOther = function(text, term) {
        if (!term) return text;
        const regex = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<mark style="background-color: #fef08a; padding: 0 2px; border-radius: 2px;">$1</mark>');
    }

    // Hook into existing navigation safely
    if (window.navigateTo) {
        const orig = window.navigateTo;
        window.navigateTo = function(viewId) {
            orig(viewId);
            if (viewId === 'view-other-disability') {
                window.renderOtherDisabilityContent();
            }
        };
    } else {
        setTimeout(() => {
            if (window.navigateTo) {
                const orig = window.navigateTo;
                window.navigateTo = function(viewId) {
                    orig(viewId);
                    if (viewId === 'view-other-disability') {
                        window.renderOtherDisabilityContent();
                    }
                };
            }
        }, 500);
    }
} catch(e) {
    alert("Real Error inside other_disability.js: " + e.message);
}
