import os
from PIL import Image

def find_colored_regions():
    images = ['assets/car_vs_car.png', 'assets/car_vs_bicycle.png', 'assets/car_vs_pedestrian.png']
    for img_path in images:
        if not os.path.exists(img_path):
            print(f"{img_path} not found")
            continue
        img = Image.open(img_path).convert('RGB')
        w, h = img.size
        
        # We want to find pixels that are colorful (high saturation)
        # Saturation can be approximated by max(R,G,B) - min(R,G,B)
        non_neutral_pixels = []
        for y in range(h):
            for x in range(w):
                r, g, b = img.getpixel((x, y))
                # If the difference is large, it's colorful (not grey/slate/white/black)
                if max(r, g, b) - min(r, g, b) > 40:
                    non_neutral_pixels.append((x, y))
                    
        if non_neutral_pixels:
            xs = [p[0] for p in non_neutral_pixels]
            ys = [p[1] for p in non_neutral_pixels]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            print(f"{img_path}: Colorful bounding box is X:[{min_x}, {max_x}], Y:[{min_y}, {max_y}]")
        else:
            print(f"{img_path}: No highly colorful pixels found")

if __name__ == '__main__':
    find_colored_regions()
