import json
import os
import urllib.request
import urllib.parse
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_image_urls(chart_no):
    # e.g. 차6-1 -> car6-1
    # 보27-1 -> man27-1
    # 거3-1 -> bic3-1
    prefix_map = {
        '차': 'car',
        '보': 'man',
        '거': 'bic'
    }
    char = chart_no[0]
    num = chart_no[1:]
    urls = []
    
    if char in prefix_map:
        urls.append(f"https://accident.knia.or.kr/video/{prefix_map[char]}{num}.png")
        
    urls.append(f"https://accident.knia.or.kr/images/capture/{urllib.parse.quote(chart_no)}_case1.PNG")
    urls.append(f"https://accident.knia.or.kr/images/capture/{urllib.parse.quote(chart_no)}_case1.png")
    return urls

def main():
    with open('c:/Users/SB/Desktop/연습용/accident_data.js', 'r', encoding='utf-8') as f:
        text = f.read().replace('window.ACCIDENT_DATA_ASYNC = ', '').strip().rstrip(';')
    data = json.loads(text)
    
    os.makedirs('c:/Users/SB/Desktop/연습용/assets/accident_images', exist_ok=True)
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    downloaded_count = 0
    failed = []
    
    print("Total charts:", len(data['details']))
    
    # Process only charts without video to save time, or ALL? 
    # User said "동영상이 들어가는 자리에 사진이 들어가 있는 경우는 전부 데이터를 받아놔서 바로구현되도록 해줘. 클릭시 개별 다운로드는 동영상에 한해서야."
    # Let's download for ALL cases because we want the fallback image to be offline-ready too!
    for i, (chart_no, detail) in enumerate(data['details'].items()):
        # Try to download image locally
        local_filename = f"assets/accident_images/{chart_no}.png"
        local_path = f"c:/Users/SB/Desktop/연습용/{local_filename}"
        
        # skip if already exists and size > 0
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            detail['imageUrl'] = local_filename
            continue
            
        success = False
        for url in get_image_urls(chart_no):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, context=ctx) as res:
                    if res.status == 200:
                        content = res.read()
                        if len(content) > 1000: # Valid image
                            with open(local_path, 'wb') as img_f:
                                img_f.write(content)
                            detail['imageUrl'] = local_filename
                            success = True
                            downloaded_count += 1
                            break
            except Exception as e:
                pass
                
        if not success:
            failed.append(chart_no)
            detail['imageUrl'] = ''
            
        if (i+1) % 50 == 0:
            print(f"Processed {i+1} charts...")

    print(f"Downloaded {downloaded_count} images. Failed: {len(failed)}")
    if failed:
        print("Failed to download images for:", failed[:10], "...")
        
    with open('c:/Users/SB/Desktop/연습용/accident_data.js', 'w', encoding='utf-8') as f:
        f.write('window.ACCIDENT_DATA_ASYNC = ')
        json.dump(data, f, ensure_ascii=False)
        f.write(';\n')

if __name__ == "__main__":
    main()
