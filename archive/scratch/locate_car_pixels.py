import os
from PIL import Image

def locate_pixels():
    img_path = 'assets/car_vs_car.png'
    if not os.path.exists(img_path):
        print(f"{img_path} not found")
        return
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    
    orange_pts = []
    blue_pts = []
    
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            # Orange range
            if r > 180 and g > 80 and g < 150 and b < 50:
                orange_pts.append((x, y))
            # Blue range
            if r < 50 and g > 100 and g < 200 and b > 180:
                blue_pts.append((x, y))
                
    if orange_pts:
        xs = [p[0] for p in orange_pts]
        ys = [p[1] for p in orange_pts]
        print(f"Orange car X range: {min(xs)} to {max(xs)}, Y range: {min(ys)} to {max(ys)}")
    else:
        print("Orange car not found")
        
    if blue_pts:
        xs = [p[0] for p in blue_pts]
        ys = [p[1] for p in blue_pts]
        print(f"Blue car X range: {min(xs)} to {max(xs)}, Y range: {min(ys)} to {max(ys)}")
    else:
        print("Blue car not found")

if __name__ == '__main__':
    locate_pixels()
