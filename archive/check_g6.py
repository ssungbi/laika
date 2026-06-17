import codecs
import json

data = json.load(codecs.open('c:/Users/SB/Desktop/연습용/grades_9902_full.json', 'r', 'utf-8'))
g6 = data[5]
print(f"Grade 6 has {len(g6['items'])} items")

# Let's look at the items to see which are "explanations"
for i, item in enumerate(g6['items']):
    desc = item['desc']
    if "항상간호" in desc or "수시간호" in desc or "장해등급분류 해설" in desc or "일상생활" in desc:
        print(f"Index {i}: {desc[:50]}")
