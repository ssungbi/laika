from bs4 import BeautifulSoup

def extract_blog_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Naver Smart Editor puts post text inside se-main-container or se-viewer
    post_area = soup.select_one('.se-main-container')
    if not post_area:
        post_area = soup.select_one('#postViewArea')
    if not post_area:
        post_area = soup.select_one('.post-view')
        
    if post_area:
        # Extract text paragraph by paragraph
        paragraphs = []
        for p in post_area.find_all(['p', 'span', 'h1', 'h2', 'h3', 'h4', 'table']):
            text = p.get_text().strip()
            if text and text not in paragraphs:
                paragraphs.append(text)
        return "\n".join(paragraphs)
    else:
        # Fallback: extract all visible text
        for s in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
            s.decompose()
        return soup.get_text()

if __name__ == '__main__':
    content_file = r"C:\Users\SB\.gemini\antigravity-ide\brain\f67f6715-6121-48bf-99e3-c5f879a79bd9\.system_generated\steps\1151\content.md"
    text = extract_blog_text(content_file)
    with open("blog_extracted_clean.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Extracted clean blog text. Length:", len(text))
    # Print preview
    print(text[:1500])
