with open('c:/Users/SB/Desktop/연습용/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_nav = False
skip_video = False

for i, line in enumerate(lines):
    if 'currentAccidentPath.length === 0' in line:
        new_lines.append(line)
        new_lines.append("""        navContainer.innerHTML = `
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
        `;\\n""")
        skip_nav = True
        continue
        
    if skip_nav:
        if 'return;' in line and '}' in lines[i+1]:
            new_lines.append(line)
            skip_nav = False
        continue

    if 'if(detail.videoUrl) {' in line:
        new_lines.append(line)
        new_lines.append("""        videoSource.src = detail.videoUrl;
        
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
        }\\n""")
        skip_video = True
        continue

    if skip_video:
        if '} else if(detail.imageUrl) {' in line:
            new_lines.append(line)
            skip_video = False
        continue

    new_lines.append(line)

with open('c:/Users/SB/Desktop/연습용/script.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
