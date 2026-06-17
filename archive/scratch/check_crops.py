import os
from PIL import Image

def analyze_crops():
    alignments = [50, 60, 70, 80, 100]
    artifacts_dir = r'C:\Users\SB\.gemini\antigravity-ide\brain\f67f6715-6121-48bf-99e3-c5f879a79bd9'
    
    for align in alignments:
        filename = f"crop_align_{align}.png"
        filepath = os.path.join(artifacts_dir, filename)
        if not os.path.exists(filepath):
            print(f"{filename} not found")
            continue
            
        img = Image.open(filepath).convert('RGB')
        w, h = img.size
        
        # Count colorful pixels in the crop
        colorful_pixels = 0
        for y in range(h):
            for x in range(w):
                r, g, b = img.getpixel((x, y))
                # Check for car-like colors (e.g. orange: high R, medium G, low B; or teal: low R, high G, high B)
                # Let's count pixels with saturation > 50
                if max(r, g, b) - min(r, g, b) > 55:
                    colorful_pixels += 1
                    
        print(f"Alignment {align}%: {colorful_pixels} colorful pixels")

if __name__ == '__main__':
    analyze_crops()
