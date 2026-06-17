import re

with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the 4 button grid with 3 button grid
old_nav_code = """    if(currentAccidentPath.length === 0) {
        navContainer.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 40px auto 0; max-width: 600px;">
                <button class="tool-card-new tc-blue" onclick="drillDownAccident('tree1', '자동차 vs 자동차 (고속도로 포함)')" style="background-image: url('assets/car_vs_car.png'); background-size: cover; background-position: center; position: relative; overflow: hidden; aspect-ratio: 4/3;">
                    <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; justify-content: center; transition: background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.3)'" onmouseout="this.style.background='rgba(0,0,0,0.5)'">
                        <span style="font-size: 2.5rem; color: #fff; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">자동차 vs 자동차</span>
                    </div>
                </button>
                <button class="tool-card-new tc-green" onclick="drillDownAccident('tree2', '자동차 vs 보행자')" style="background-image: url('assets/car_vs_pedestrian.png'); background-size: cover; background-position: center; position: relative; overflow: hidden; aspect-ratio: 4/3;">
                    <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; justify-content: center; transition: background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.3)'" onmouseout="this.style.background='rgba(0,0,0,0.5)'">
                        <span style="font-size: 2.5rem; color: #fff; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">자동차 vs 보행자</span>
                    </div>
                </button>
                <button class="tool-card-new tc-orange" onclick="drillDownAccident('tree3', '자동차 vs 이륜차')" style="background-image: url('assets/car_vs_motorcycle.png'); background-size: cover; background-position: center; position: relative; overflow: hidden; aspect-ratio: 4/3;">
                    <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; justify-content: center; transition: background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.3)'" onmouseout="this.style.background='rgba(0,0,0,0.5)'">
                        <span style="font-size: 2.5rem; color: #fff; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">자동차 vs 이륜차</span>
                    </div>
                </button>
                <button class="tool-card-new tc-purple" onclick="drillDownAccident('tree4', '자동차 vs 자전거')" style="background-image: url('assets/car_vs_bicycle.png'); background-size: cover; background-position: center; position: relative; overflow: hidden; aspect-ratio: 4/3;">
                    <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; justify-content: center; transition: background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.3)'" onmouseout="this.style.background='rgba(0,0,0,0.5)'">
                        <span style="font-size: 2.5rem; color: #fff; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">자동차 vs 자전거</span>
                    </div>
                </button>
            </div>
        `;
        return;
    }"""

new_nav_code = """    if(currentAccidentPath.length === 0) {
        navContainer.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 40px auto 0; max-width: 900px;">
                <button class="tool-card-new tc-blue" onclick="drillDownAccident('tree1', '자동차 vs 자동차 (고속도로 포함)')" style="background-image: url('assets/car_vs_car.png'); background-size: cover; background-position: center; position: relative; overflow: hidden; aspect-ratio: 4/3;">
                    <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; justify-content: center; transition: background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.3)'" onmouseout="this.style.background='rgba(0,0,0,0.5)'">
                        <span style="font-size: 2rem; color: #fff; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">자동차 vs 자동차</span>
                    </div>
                </button>
                <button class="tool-card-new tc-purple" onclick="drillDownAccident('tree4', '자동차 vs 자전거')" style="background-image: url('assets/car_vs_bicycle.png'); background-size: cover; background-position: center; position: relative; overflow: hidden; aspect-ratio: 4/3;">
                    <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; justify-content: center; transition: background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.3)'" onmouseout="this.style.background='rgba(0,0,0,0.5)'">
                        <span style="font-size: 2rem; color: #fff; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">자동차 vs 자전거</span>
                    </div>
                </button>
                <button class="tool-card-new tc-green" onclick="drillDownAccident('tree2', '자동차 vs 보행자')" style="background-image: url('assets/car_vs_pedestrian.png'); background-size: cover; background-position: center; position: relative; overflow: hidden; aspect-ratio: 4/3;">
                    <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; justify-content: center; transition: background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.3)'" onmouseout="this.style.background='rgba(0,0,0,0.5)'">
                        <span style="font-size: 2rem; color: #fff; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">자동차 vs 보행자</span>
                    </div>
                </button>
            </div>
        `;
        return;
    }"""

if old_nav_code in text:
    text = text.replace(old_nav_code, new_nav_code)
else:
    print("WARNING: Could not find old nav code!")

# Update showAccidentChart to handle video errors and autoplay
old_video_code = """    if(detail.videoUrl) {
        videoSource.src = detail.videoUrl;
        videoElement.load();
        videoElement.style.display = 'block';
        imageElement.style.display = 'none';
    } else if(detail.imageUrl) {"""

new_video_code = """    if(detail.videoUrl) {
        videoSource.src = detail.videoUrl;
        
        // Handle broken videos from KNIA server (e.g. 314.mp4)
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
        
        // Try autoplaying since user interacted to reach here
        let playPromise = videoElement.play();
        if (playPromise !== undefined) {
            playPromise.catch(error => {
                console.log("Autoplay blocked or video missing", error);
                // Fallback handled by onerror
            });
        }
    } else if(detail.imageUrl) {"""

if old_video_code in text:
    text = text.replace(old_video_code, new_video_code)
else:
    print("WARNING: Could not find old video code!")

with open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("script.js updated successfully.")
