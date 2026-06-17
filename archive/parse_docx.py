import zipfile
import xml.etree.ElementTree as ET

def extract_text_from_docx(path):
    try:
        doc = zipfile.ZipFile(path)
        xml_content = doc.read('word/document.xml')
        doc.close()
        tree = ET.XML(xml_content)
        
        # XML namespace for Word processing
        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = WORD_NAMESPACE + 'p'
        TEXT = WORD_NAMESPACE + 't'
        
        paragraphs = []
        for paragraph in tree.iter(PARA):
            texts = [node.text for node in paragraph.iter(TEXT) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error: {e}"

text = extract_text_from_docx('c:/Users/SB/Desktop/연습용/장해분류표_0505~1803.docx')
with open('c:/Users/SB/Desktop/연습용/parsed_0505.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("Parsed successfully. Check parsed_0505.txt")
