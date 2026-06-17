import codecs

for fn in ['recovered_v9902.txt', 'found_v9902.txt', 'test.txt']:
    try:
        text = codecs.open(f'c:/Users/SB/Desktop/연습용/{fn}', 'r', 'utf-8').read()
        print(f"--- {fn} (size: {len(text)}) ---")
        print(text[:200].encode('utf-8', 'ignore').decode('utf-8'))
        print("\n")
    except Exception as e:
        print(f"Error on {fn}: {e}")
