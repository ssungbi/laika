import os
from PIL import Image

def find_car_y_coords():
    img_path = 'assets/car_vs_car.png'
    if not os.path.exists(img_path):
        print(f"{img_path} not found")
        return
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    
    orange_pixels = []
    blue_pixels = []
    
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            # Orange car color range: highly saturated orange
            if r > 180 and g > 80 and g < 150 and b < 50:
                orange_pixels.append((x, y))
            # Blue car color range: highly saturated blue/teal
            if r < 50 and g > 100 and g < 200 and b > 180:
                blue_pixels.append((x, y))
                
    if orange_pixels:
        ys = [p[1] for p in orange_pixels]
        print(f"Orange car Y range: {min(ys)} to {max(ys)}")
    else:
        print("Orange car not found by color filter")
        
    if blue_pixels:
        ys = [p[1] for p in blue_pixels]
        print(f"Blue car Y range: {min(ys)} to {max(ys)}")
    else:
        print("Blue car not found by color filter")

if __name__ == '__main__':
    find_car_y_coords()
