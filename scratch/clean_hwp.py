import re

def clean_hwp_text(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # HWP files decompressed streams contain binary tags and control codes.
    # Let's filter out non-printable ascii/hangul characters and keep legible sentences.
    
    # Strip binary garbage characters
    # Keep Korean (Hangul), alphabetic characters, digits, spaces, and standard punctuation.
    cleaned = []
    # Let's split by nulls or control chars
    for chunk in re.split(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]+', content):
        chunk = chunk.strip()
        if not chunk:
            continue
        # Remove weird characters like surrogate pairs or binary symbols
        chunk = re.sub(r'[\u0080-\u00ff\uf000-\uf0ff\ue000-\uefff]', '', chunk)
        # Collapse multiple spaces/newlines
        chunk = re.sub(r'\s+', ' ', chunk).strip()
        if len(chunk) > 2:
            cleaned.append(chunk)
            
    # Write as lines
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in cleaned:
            # Let's add newline before headers
            if any(h in line for h in ["장례비", "위자료", "상실수익액", "휴업손해", "간병비", "지급기준", "노동능력상실률"]):
                f.write("\n")
            f.write(line + "\n")

if __name__ == '__main__':
    clean_hwp_text("hwp_extracted.txt", "hwp_clean.txt")
    print("HWP file cleaned and saved to hwp_clean.txt")
