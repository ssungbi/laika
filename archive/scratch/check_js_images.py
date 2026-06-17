import os

def check_all_js():
    js_files = [f for f in os.listdir('.') if f.endswith('.js')]
    images = ["가슴뼈.png", "골반뼈.png", "발가락.png", "손가락.png"]
    
    for jsf in js_files:
        try:
            with open(jsf, 'r', encoding='utf-8') as f:
                content = f.read()
            for img in images:
                if img in content:
                    print(f"{img} is referenced in {jsf}")
        except Exception as e:
            print(f"Error reading {jsf}: {e}")

if __name__ == '__main__':
    check_all_js()
