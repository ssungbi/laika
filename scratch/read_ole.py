import os
import sys
import zlib

try:
    import olefile
except ImportError:
    print("olefile module not found. Attempting to run via pip or using alternative method.")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "olefile"])
    import olefile

def extract_hwp_text(hwp_path):
    if not olefile.isOleFile(hwp_path):
        print("Not a valid OLE file")
        return ""
    
    ole = olefile.OleFileIO(hwp_path)
    dirs = ole.listdir()
    
    # BodyText stream contains the content
    bodytext_dirs = [d for d in dirs if d[0] == 'BodyText']
    
    text_content = []
    for d in bodytext_dirs:
        stream_path = '/'.join(d)
        stream = ole.openstream(d)
        data = stream.read()
        
        # HWP BodyText is typically compressed with zlib (deflate)
        try:
            decompressed = zlib.decompress(data, -15) # raw deflate
        except Exception:
            try:
                decompressed = zlib.decompress(data) # standard zlib
            except Exception as e:
                print(f"Failed to decompress {stream_path}: {e}")
                continue
                
        # Decompressed data contains text and formatting tokens.
        # Let's decode as UTF-16LE (Korean standard HWP encoding for HWP5)
        try:
            text = decompressed.decode('utf-16le', errors='ignore')
            text_content.append(text)
        except Exception as e:
            print(f"Failed to decode: {e}")
            
    return "\n".join(text_content)

if __name__ == '__main__':
    hwp_file = "별표 1 대인배상, 무보험자동차에 의한 상해 지급 기준.hwp"
    if os.path.exists(hwp_file):
        text = extract_hwp_text(hwp_file)
        # Clean up some binary junk/headers if possible, or just write it out
        with open("hwp_extracted.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted content to hwp_extracted.txt. Length: {len(text)}")
        # Print first 1000 characters
        print("=== PREVIEW ===")
        print(text[:1000])
    else:
        print(f"File not found: {hwp_file}")
