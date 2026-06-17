import json

with open(r'c:\Users\SB\Desktop\연습용\mcbride_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# The user explicitly mapped the categories:
# Sheet 1: 절단 - 절단
# Sheet 2-10: 관절강직
# Sheet 11-20: 골절 (Wait, the user said "골절 중분류 : 쇄골 견갑골상완골 '요골,척골' 손목뼈 손가락뼈 골반 대퇴골 '경골,비골' 족부골절" -> That's 9 items. Let's see: 11(쇄골), 12(견갑골), 13(상완골), 14(요골,척골), 15(손목뼈), 16(손가락뼈), 17(골반), 18(대퇴골), 19(경골과 비골), 20(족부골절) -> 10 items. "견갑골상완골" might mean 견갑골 and 상완골 merged or just two things. Let's map exactly as requested.)

# Let's override the major and minor for each index.
mapping = {
    0: ("절단", "절단"),
    1: ("관절강직", "견관절"),
    2: ("관절강직", "주관절"),
    3: ("관절강직", "수관절"),
    4: ("관절강직", "엄지손가락"),
    5: ("관절강직", "기타손가락"),
    6: ("관절강직", "고관절"),
    7: ("관절강직", "슬관절"),
    8: ("관절강직", "족관절"),
    9: ("관절강직", "발가락"),
    10: ("골절", "쇄골"),
    11: ("골절", "견갑골"),
    12: ("골절", "상완골"),
    13: ("골절", "요골,척골"),
    14: ("골절", "손목뼈"),
    15: ("골절", "손가락뼈"),
    16: ("골절", "골반"),
    17: ("골절", "대퇴골"),
    18: ("골절", "경골,비골"),
    19: ("골절", "족부골절"),
    20: ("기타", "척추손상"),
    21: ("기타", "말초신경"),
    22: ("기타", "복부"),
    23: ("기타", "여성생식기"),
    24: ("기타", "직장"),
    25: ("기타", "비뇨,생식기"),
    26: ("기타", "관절염"),
    27: ("기타", "결핵"),
    28: ("기타", "흉곽의손상"),
    29: ("기타", "심장질환심혈관계"),
    30: ("기타", "두부,뇌,척수"),
    31: ("기타", "안면"),
    32: ("기타", "귀")
}

for i, item in enumerate(d):
    if i in mapping:
        item['major'] = mapping[i][0]
        item['minor'] = mapping[i][1]

with open(r'c:\Users\SB\Desktop\연습용\mcbride_data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("Updated mcbride_data.json mapping successfully.")
