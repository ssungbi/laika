import re

with open('c:/Users/SB/Desktop/연습용/build_accident_data.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add imports
text = text.replace('import time\nfrom bs4 import BeautifulSoup', 'import time\nimport os\nimport random\nfrom bs4 import BeautifulSoup')

# Add download_media
fetch_url_end = text.find('def parse_tree_from_html')
download_media_func = """
def download_media(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path):
        return
    req = urllib.request.Request(url, headers=headers)
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, context=ctx) as res:
                content_bytes = res.read()
                with open(local_path, 'wb') as f:
                    f.write(content_bytes)
                return
        except Exception as e:
            time.sleep(1)

"""
text = text[:fetch_url_end] + download_media_func + text[fetch_url_end:]

# Replace video logic
old_video = """    video_source = soup.select_one('source[type="video/mp4"]')
    if video_source and video_source.get('src'):
        detail['videoUrl'] = "https://accident.knia.or.kr" + video_source['src']
    else:
        detail['imageUrl'] = f"https://accident.knia.or.kr/images/capture/{urllib.parse.quote(chartNo)}_case1.PNG"
"""

new_video = """    video_source = soup.select_one('source[type="video/mp4"]')
    chart_no_safe = urllib.parse.quote(chartNo).replace('%', '_')
    if video_source and video_source.get('src'):
        original_url = "https://accident.knia.or.kr" + video_source['src']
        local_filename = f"media/{chart_no_safe}.mp4"
        download_media(original_url, local_filename)
        detail['videoUrl'] = local_filename
    else:
        original_url = f"https://accident.knia.or.kr/images/capture/{urllib.parse.quote(chartNo)}_case1.PNG"
        local_filename = f"media/{chart_no_safe}.PNG"
        download_media(original_url, local_filename)
        detail['imageUrl'] = local_filename
"""
text = text.replace(old_video, new_video)

# Replace sleep
text = text.replace('time.sleep(0.05)', 'delay = random.uniform(1.5, 3.0)\n        print(f"Waiting {delay:.2f} seconds to avoid IP block...")\n        time.sleep(delay)')

with open('c:/Users/SB/Desktop/연습용/build_accident_data.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated build_accident_data.py")
