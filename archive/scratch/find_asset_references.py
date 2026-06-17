import os

def check_image_references():
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg')
    images = [f for f in os.listdir('.') if f.lower().endswith(image_extensions)]
    
    code_files = ['index.html', 'styles.css', 'script.js']
    file_contents = {}
    for cf in code_files:
        if os.path.exists(cf):
            with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
                file_contents[cf] = f.read()
                
    print("Found active image references:")
    for img in images:
        referenced = False
        for cf, content in file_contents.items():
            if img in content:
                print(f"  - {img} is referenced in {cf}")
                referenced = True
        if not referenced:
            print(f"  - {img} is NOT referenced in any code files.")

if __name__ == '__main__':
    check_image_references()
