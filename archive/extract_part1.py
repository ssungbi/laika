import pdfplumber
import json

pdf1_path = r"C:\Users\SB\Downloads\0.상해급수 해설서(2019.01.24)_part1.pdf"

classes_data = []

with pdfplumber.open(pdf1_path) as pdf:
    current_grade = ""
    current_amount = ""
    current_part = ""
    
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                # row is [상해급별, 한도금액, 부위, 상해내용]
                # Sometimes headers or empty rows appear
                if len(row) >= 4:
                    grade = row[0]
                    amount = row[1]
                    part = row[2]
                    desc = row[3]
                    
                    if grade and "급" in grade:
                        current_grade = grade.replace("\n", "")
                    if amount and "만" in amount:
                        current_amount = amount.replace("\n", "")
                    if part and part.strip():
                        current_part = part.replace("\n", "")
                        
                    if desc and desc.strip() and current_grade:
                        desc_clean = desc.replace("\n", " ").strip()
                        if desc_clean == "상해내용" or "해당한다고 인정되는" in desc_clean and not grade:
                            pass # skip header
                            
                        # find if current_grade exists in classes_data
                        grade_obj = next((item for item in classes_data if item["grade"] == current_grade), None)
                        if not grade_obj:
                            grade_obj = {"grade": current_grade, "amount": current_amount, "items": []}
                            classes_data.append(grade_obj)
                            
                        grade_obj["items"].append({"part": current_part, "desc": desc_clean})

with open("injury_data_extracted.json", "w", encoding="utf-8") as f:
    json.dump(classes_data, f, ensure_ascii=False, indent=2)

print("Extracted classes:", len(classes_data))
for c in classes_data:
    print(f"{c['grade']}: {len(c['items'])} items")
