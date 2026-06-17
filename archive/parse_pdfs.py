import pdfplumber
import json
import os

pdf1_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part1.pdf"
pdf2_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part2.pdf"

try:
    with pdfplumber.open(pdf1_path) as pdf:
        text1 = ""
        for page in pdf.pages:
            text1 += page.extract_text() + "\n"
    with open("temp_dump1.txt", "w", encoding="utf-8") as f:
        f.write(text1[:2000]) # write prefix to check
    print("Successfully read part1.pdf")
except Exception as e:
    print(f"Error: {e}")
