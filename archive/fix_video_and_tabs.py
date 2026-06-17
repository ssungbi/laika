import re

with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the broken video logic in showAccidentChart
old_video_logic = """    const videoSource = document.getElementById('accident-video-source');
    const videoElement = document.getElementById('accident-video');
    const imageElement = document.getElementById('accident-image');
    
    if(detail.videoUrl) {
        videoSource.src = detail.videoUrl;
        
        videoElement.onerror = function() {
            console.warn("Video failed to load:", detail.videoUrl);
            videoElement.style.display = 'none';
            if (detail.imageUrl) {
                imageElement.src = detail.imageUrl;
                imageElement.style.display = 'block';
            }
        };

        videoElement.load();
        videoElement.style.display = 'block';
        imageElement.style.display = 'none';
        
        let playPromise = videoElement.play();
        if (playPromise !== undefined) {
            playPromise.catch(error => {
                console.log("Autoplay blocked or video missing", error);
            });
        }
    } else if(detail.imageUrl) {
        videoElement.style.display = 'none';
        imageElement.src = detail.imageUrl;
        imageElement.style.display = 'block';
    } else {
        videoElement.style.display = 'none';
        imageElement.style.display = 'none';
    }"""

new_video_logic = """    const imageContainer = document.getElementById('acc-detail-image');
    
    if(detail.videoUrl) {
        imageContainer.innerHTML = `
            <video id="accident-video" controls style="width: 100%; max-height: 100%;">
                <source src="${detail.videoUrl}" type="video/mp4">
                브라우저가 동영상을 지원하지 않습니다.
            </video>
        `;
        const videoElement = document.getElementById('accident-video');
        videoElement.addEventListener('error', function(e) {
            console.warn("Video failed to load:", detail.videoUrl);
            if (detail.imageUrl) {
                imageContainer.innerHTML = `<img src="${detail.imageUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;
            } else {
                imageContainer.innerHTML = `<span style="color: #94a3b8;">도표 이미지가 없습니다.</span>`;
            }
        }, true);
        
        let playPromise = videoElement.play();
        if (playPromise !== undefined) {
            playPromise.catch(error => {
                console.log("Autoplay blocked or video missing", error);
            });
        }
    } else if(detail.imageUrl) {
        imageContainer.innerHTML = `<img src="${detail.imageUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain;">`;
    } else {
        imageContainer.innerHTML = `<span style="color: #94a3b8;">도표 이미지가 없습니다.</span>`;
    }"""

if old_video_logic in text:
    text = text.replace(old_video_logic, new_video_logic)
else:
    print("WARNING: Could not find old video logic to replace!")

# Also make sure window.currentAccidentDetail is set
old_chart_no_line = "    document.getElementById('acc-detail-chart-no').innerText = detail.chartNo || chartNo;"
new_chart_no_line = "    document.getElementById('acc-detail-chart-no').innerText = detail.chartNo || chartNo;\n    window.currentAccidentDetail = detail;\n    switchAccidentDetailTab('situation'); // reset tab"

if old_chart_no_line in text and "window.currentAccidentDetail = detail;" not in text:
    text = text.replace(old_chart_no_line, new_chart_no_line)

# Append switchAccidentDetailTab
tab_logic = """
function switchAccidentDetailTab(tab) {
    const btnSituation = document.getElementById('acc-tab-situation');
    const btnApply = document.getElementById('acc-tab-apply');
    const btnExplain = document.getElementById('acc-tab-explain');
    const contentDiv = document.getElementById('acc-detail-situation');
    
    if(!btnSituation || !btnApply || !btnExplain || !contentDiv) return;
    
    // Reset buttons
    btnSituation.style.fontWeight = 'normal'; btnSituation.style.color = '#64748b'; btnSituation.style.background = 'transparent';
    btnApply.style.fontWeight = 'normal'; btnApply.style.color = '#64748b'; btnApply.style.background = 'transparent';
    btnExplain.style.fontWeight = 'normal'; btnExplain.style.color = '#64748b'; btnExplain.style.background = 'transparent';
    
    let detail = window.currentAccidentDetail;
    let htmlContent = '내용이 없습니다.';
    
    if (tab === 'situation') {
        btnSituation.style.fontWeight = 'bold'; btnSituation.style.color = '#0f766e'; btnSituation.style.background = '#fff';
        htmlContent = detail && detail.tab_situation ? detail.tab_situation : (detail && detail.situation ? detail.situation : (detail && detail.title ? detail.title : '사고 상황 내용이 없습니다.'));
    } else if (tab === 'apply') {
        btnApply.style.fontWeight = 'bold'; btnApply.style.color = '#0f766e'; btnApply.style.background = '#fff';
        htmlContent = detail && detail.tab_apply ? detail.tab_apply : '적용 내용이 없습니다.';
    } else if (tab === 'explain') {
        btnExplain.style.fontWeight = 'bold'; btnExplain.style.color = '#0f766e'; btnExplain.style.background = '#fff';
        htmlContent = detail && detail.tab_explain ? detail.tab_explain : '해설 내용이 없습니다.';
    }
    
    contentDiv.innerHTML = htmlContent;
}
"""

if "function switchAccidentDetailTab" not in text:
    text += tab_logic

with open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("script.js video logic and tabs fixed!")
