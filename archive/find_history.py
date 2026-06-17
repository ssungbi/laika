import os
import time

appdata = os.environ.get('APPDATA', '')
history_dirs = [
    os.path.join(appdata, 'Code', 'User', 'History'),
    os.path.join(appdata, 'Cursor', 'User', 'History'),
    os.path.join(appdata, 'VSCodium', 'User', 'History')
]

now = time.time()
candidates = []

for h_dir in history_dirs:
    if not os.path.exists(h_dir):
        continue
    for root, dirs, files in os.walk(h_dir):
        for f in files:
            if f != 'entries.json':
                path = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(path)
                    if now - mtime < 24 * 3600:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                            content = file.read()
                            if 'view-neo' in content or 'view-kcd' in content or 'disability-period' in content:
                                candidates.append((mtime, path, len(content)))
                except Exception:
                    pass

candidates.sort(reverse=True)
print(f"Found {len(candidates)} candidates.")
for m, p, l in candidates[:15]:
    print(f'Mtime: {m}, Size: {l}, Path: {p}')
    with open(p, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        if '신생물' in content or '질병' in content:
            print('  -> CONTAINS VALID KOREAN!')
            with open('index_recovered.html', 'w', encoding='utf-8') as out:
                out.write(content)
            print('  -> Recovered to index_recovered.html')
            break
