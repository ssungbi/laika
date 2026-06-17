import json
import re
import os

def clean_category(name):
    # Remove leading emoji/icon
    name = re.sub(r'^🟥\s*', '', name)
    return name.strip()

def process_data():
    # Load 1-3 types data
    with open("scratch/surgery_13_data.json", "r", encoding="utf-8") as f:
        data_13 = json.load(f)
        
    parts_13 = []
    current_part = None
    
    for row in data_13["rows"]:
        if len(row) == 1:
            part_name = clean_category(row[0])
            current_part = {"part": part_name, "items": []}
            parts_13.append(current_part)
        elif len(row) == 2 and current_part is not None:
            name, grade = row[0], row[1]
            if grade.strip():
                grade_str = f"{grade.strip()}종"
            else:
                grade_str = ""
            current_part["items"].append({"name": name.strip(), "grade": grade_str})
            
    # Group 1-3 by grade
    grades_13_dict = {}
    for part_obj in parts_13:
        for item in part_obj["items"]:
            if not item["grade"]:
                continue
            g = item["grade"]
            if g not in grades_13_dict:
                grades_13_dict[g] = []
            grades_13_dict[g].append({"part": part_obj["part"], "name": item["name"]})
            
    grades_13 = []
    # Sort keys: 1종, 2종, 3종
    for g in sorted(grades_13_dict.keys()):
        grades_13.append({"grade": g, "items": grades_13_dict[g]})
        
    # Load 1-5 types data
    with open("scratch/surgery_15_data.json", "r", encoding="utf-8") as f:
        data_15 = json.load(f)
        
    parts_15 = []
    current_part = None
    
    for row in data_15["rows"]:
        if len(row) == 1:
            part_name = clean_category(row[0])
            # Custom replacement for 1~5종 skeletal category
            display_part_name = part_name
            grade_part_name = part_name
            if "근골" in part_name and "발정술" in part_name:
                display_part_name = "근골(筋骨)의 수술 (발정술 등 내고정물 제거술, 치과처치 및 수술은 제외)"
                grade_part_name = "근골(筋骨)의 수술"
            elif "시각기" in part_name and "약물주입" in part_name:
                grade_part_name = "시각기의 수술"
            elif "비뇨기계" in part_name and "인공임신" in part_name:
                grade_part_name = "비뇨기계· 생식기계의 수술"
            elif "상기 이외" in part_name and "검사" in part_name:
                grade_part_name = "상기 이외의 수술"
            current_part = {"part": display_part_name, "grade_part": grade_part_name, "items": []}
            parts_15.append(current_part)
        elif len(row) == 2 and current_part is not None:
            name, grade = row[0], row[1]
            if grade.strip():
                grade_str = f"{grade.strip()}종"
            else:
                grade_str = ""
            current_part["items"].append({"name": name.strip(), "grade": grade_str})
            
    # Group 1-5 by grade
    grades_15_dict = {}
    for part_obj in parts_15:
        part_name_for_grade = part_obj.get("grade_part", part_obj["part"])
        for item in part_obj["items"]:
            if not item["grade"]:
                continue
            g = item["grade"]
            if g not in grades_15_dict:
                grades_15_dict[g] = []
            grades_15_dict[g].append({"part": part_name_for_grade, "name": item["name"]})
            
    grades_15 = []
    # Sort keys: 1종, 2종, 3종, 4종, 5종
    for g in sorted(grades_15_dict.keys()):
        grades_15.append({"grade": g, "items": grades_15_dict[g]})
        
    # Load search data
    with open("scratch/surgery_search_data.json", "r", encoding="utf-8") as f:
        search_json = json.load(f)
        
    search_list = []
    for row in search_json["rows"]:
        if len(row) >= 3:
            search_list.append({
                "name": row[0].strip(),
                "class13": row[1].strip(),
                "class15": row[2].strip()
            })
            
    # Write to surgery_data.js
    js_content = f"""// Operation Classification Table Data
const SURGERY_SEARCH_DATA = {json.dumps(search_list, ensure_ascii=False, indent=2)};

const SURGERY_13_DATA = {{
  parts: {json.dumps(parts_13, ensure_ascii=False, indent=2)},
  grades: {json.dumps(grades_13, ensure_ascii=False, indent=2)}
}};

const SURGERY_15_DATA = {{
  parts: {json.dumps(parts_15, ensure_ascii=False, indent=2)},
  grades: {json.dumps(grades_15, ensure_ascii=False, indent=2)}
}};
"""
    
    with open("surgery_data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print("Successfully built surgery_data.js!")
    print(f"Search list length: {len(search_list)}")
    print(f"1-3 Parts length: {len(parts_13)}")
    print(f"1-5 Parts length: {len(parts_15)}")

if __name__ == '__main__':
    process_data()
