import re

with open('c:/Users/SB/Desktop/연습용/build_accident_data.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove download_media function entirely as it's no longer needed
download_media_pattern = re.compile(r'def download_media\(url, local_path\):.*?def parse_tree_from_html', re.DOTALL)
text = download_media_pattern.sub('def parse_tree_from_html', text)

# Replace extract_chart_detail video logic
old_video = """    video_source = soup.select_one('source[type="video/mp4"]')
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
        detail['imageUrl'] = local_filename"""

new_video = """    video_source = soup.select_one('source[type="video/mp4"]')
    if video_source and video_source.get('src'):
        detail['videoUrl'] = "https://accident.knia.or.kr" + video_source['src']
    else:
        detail['imageUrl'] = f"https://accident.knia.or.kr/images/capture/{urllib.parse.quote(chartNo)}_case1.PNG" """
text = text.replace(old_video, new_video)

# Replace main function
start_idx = text.find('def main():')

new_main = """def main():
    data = { 'details': {} }
    charts_to_fetch = []
    
    def find_charts(nodes):
        for n in nodes:
            if n['type'] == 'chart':
                charts_to_fetch.append(n)
            elif 'children' in n:
                find_charts(n['children'])
    
    category_names = {
        1: "Car vs Car",
        2: "Car vs Pedestrian",
        3: "Car vs Two-Wheeler",
        4: "Car vs Bicycle",
        5: "Highway"
    }

    for i in range(1, 6):
        print(f"Scraping {category_names[i]} (myaccident{i})...")
        html = fetch_url(f'https://accident.knia.or.kr/myaccident{i}')
        if not html:
            print(f"Failed to fetch myaccident{i}")
            data[f'tree{i}'] = []
            continue
        tree = parse_tree_from_html(html, i)
        data[f'tree{i}'] = tree

    # Merge tree5 into tree1
    if 'tree5' in data and data['tree5']:
        highway_node = {'id': 'highway_merged', 'text': '고속도로/자동차전용도로', 'children': data['tree5'], 'type': 'category'}
        data['tree1'].append(highway_node)
        del data['tree5']
    
    # Collect all charts
    for i in range(1, 5):
        if f'tree{i}' in data:
            find_charts(data[f'tree{i}'])

    total_charts = len(charts_to_fetch)
    print(f"Found a total of {total_charts} charts.")
    
    for i, c in enumerate(charts_to_fetch):
        print(f"Fetching detail for {c['chartNo']} ({i+1}/{total_charts})...")
        detail = extract_chart_detail(c['chartNo'], c['chartType'])
        if detail:
            data['details'][c['chartNo']] = detail
        delay = random.uniform(1.0, 2.0)
        print(f"Waiting {delay:.2f} seconds to avoid IP block...")
        time.sleep(delay)
        
    with open('accident_data.js', 'w', encoding='utf-8') as f:
        f.write('window.ACCIDENT_DATA_ASYNC = ')
        json.dump(data, f, ensure_ascii=False)
        f.write(';\\n')
        
    print("Scraping complete. Saved to accident_data.js")

if __name__ == "__main__":
    main()
"""

new_text = text[:start_idx] + new_main

with open('c:/Users/SB/Desktop/연습용/build_accident_data.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("build_accident_data.py updated successfully.")
