import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def search_word(file_path, word):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f, 1):
            if word in line:
                print(f"{os.path.basename(file_path)}:{idx}: {line.strip()}")

search_word("index.html", "162")
search_word("index.html", "4,057")
search_word("index.html", "4057")
