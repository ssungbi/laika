import codecs

script_text = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

# Fix 1: 총칙
old_chongchik = "⑨ 다리 \uf0289\uf0292\uf0289 손가락 \uf0289\uf0293 발가락 \uf0289\uf0294 흉·복부장기 및 비뇨생식기 \uf0289\uf0295 신경계·정신행동"
new_chongchik = "⑨ 다리 ⑩ 손가락 ⑪ 발가락 ⑫ 흉·복부장기 및 비뇨생식기 ⑬ 신경계·정신행동"

script_text = script_text.replace(old_chongchik, new_chongchik)

# Fix 2: 눈의 장해 items
old_eye_4 = '"desc": "4)          “        0.06      ”",'
new_eye_4 = '"desc": "4) 한 눈의 교정시력이 0.06 이하로 된 때",'
old_eye_5 = '"desc": "5)          “         0.1      ”",'
new_eye_5 = '"desc": "5) 한 눈의 교정시력이 0.1 이하로 된 때",'
old_eye_6 = '"desc": "6)          “         0.2      ”",'
new_eye_6 = '"desc": "6) 한 눈의 교정시력이 0.2 이하로 된 때",'

script_text = script_text.replace(old_eye_4, new_eye_4)
script_text = script_text.replace(old_eye_5, new_eye_5)
script_text = script_text.replace(old_eye_6, new_eye_6)

codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script_text)
print("Data fixes applied.")
