import codecs

for fn in ['recovered_v9902.txt', 'found_v9902.txt', 'test.txt']:
    try:
        text = codecs.open(f'c:/Users/SB/Desktop/연습용/{fn}', 'r', 'utf-8').read()
        if '"v1804": [' in text:
            print(f"Found v1804 in {fn}")
        else:
            print(f"Not in {fn}")
    except Exception as e:
        print(f"Error on {fn}: {e}")
