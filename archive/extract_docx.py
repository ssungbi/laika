import zipfile
import re
import xml.etree.ElementTree as ET
import codecs

def extract_text_from_docx(docx_path, txt_path):
    # Open the docx file as a zip file
    try:
        with zipfile.ZipFile(docx_path) as z:
            # Read the document.xml file
            xml_content = z.read('word/document.xml')
            
            # Parse the XML
            root = ET.fromstring(xml_content)
            
            # Define the namespace for Word XML
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Extract text from all <w:t> tags
            text_lines = []
            
            # Find all paragraph tags <w:p>
            for p in root.findall('.//w:p', ns):
                p_text = []
                # Find all text tags <w:t> within the paragraph
                for t in p.findall('.//w:t', ns):
                    if t.text:
                        p_text.append(t.text)
                
                # Join the text parts of the paragraph and append to lines
                if p_text:
                    text_lines.append(''.join(p_text))
                else:
                    # Empty paragraph, append empty line
                    text_lines.append('')
            
            # Write to txt file
            with codecs.open(txt_path, 'w', 'utf-8') as f:
                f.write('\n'.join(text_lines))
                
            print(f"Successfully extracted text to {txt_path}")
            
    except Exception as e:
        print(f"Error: {e}")

extract_text_from_docx('c:/Users/SB/Desktop/연습용/장해분류표_최신.docx', 'c:/Users/SB/Desktop/연습용/parsed_latest.txt')
