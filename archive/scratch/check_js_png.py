import os

def check_png_references():
    js_files = [f for f in os.listdir('.') if f.endswith('.js')]
    for jsf in js_files:
        with open(jsf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if '.png' in content:
            print(f"Found .png in {jsf}:")
            for line in content.split('\n'):
                if '.png' in line:
                    print(f"  {line.strip()}")

if __name__ == '__main__':
    check_png_references()
