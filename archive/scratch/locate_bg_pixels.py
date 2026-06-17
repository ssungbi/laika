import os
from PIL import Image

def locate_background_elements():
    img_path = 'assets/car_vs_car.png'
    if not os.path.exists(img_path):
        print(f"{img_path} not found")
        return
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    
    green_pts = []
    brown_pts = []
    
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            # Green tree: highly green
            if g > 120 and r < 100 and b < 100:
                green_pts.append((x, y))
            # Brown building: medium R, medium-low G, low B
            if r > 100 and r < 200 and g > 60 and g < 130 and b > 40 and b < 100:
                brown_pts.append((x, y))
                
    if green_pts:
        xs = [p[0] for p in green_pts]
        ys = [p[1] for p in green_pts]
        print(f"Tree (Green) X range: {min(xs)} to {max(xs)}, Y range: {min(ys)} to {max(ys)}")
    else:
        print("Tree not found")
        
    if brown_pts:
        xs = [p[0] for p in brown_pts]
        ys = [p[1] for p in brown_pts]
        print(f"Building (Brown) X range: {min(xs)} to {max(xs)}, Y range: {min(ys)} to {max(ys)}")
    else:
        print("Building not found")

if __name__ == '__main__':
    locate_background_elements()
