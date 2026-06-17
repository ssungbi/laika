import os
from PIL import Image

def locate_other_pixels():
    # Bicycle image
    bike_path = 'assets/car_vs_bicycle.png'
    if os.path.exists(bike_path):
        img = Image.open(bike_path).convert('RGB')
        w, h = img.size
        # Bicycle or rider colors (typically yellow/orange/blue)
        yellow_pts = []
        for y in range(h):
            for x in range(w):
                r, g, b = img.getpixel((x, y))
                if r > 180 and g > 150 and b < 50:
                    yellow_pts.append((x, y))
        if yellow_pts:
            xs = [p[0] for p in yellow_pts]
            ys = [p[1] for p in yellow_pts]
            print(f"Bicycle yellow range: X: {min(xs)} to {max(xs)}, Y: {min(ys)} to {max(ys)}")
        else:
            print("Bicycle yellow not found")
            
    # Pedestrian image
    ped_path = 'assets/car_vs_pedestrian.png'
    if os.path.exists(ped_path):
        img = Image.open(ped_path).convert('RGB')
        w, h = img.size
        # Pedestrian colors (typically yellow, orange, red, blue)
        color_pts = []
        for y in range(h):
            for x in range(w):
                r, g, b = img.getpixel((x, y))
                if r > 150 and g < 100 and b < 100: # red-like
                    color_pts.append((x, y))
        if color_pts:
            xs = [p[0] for p in color_pts]
            ys = [p[1] for p in color_pts]
            print(f"Pedestrian red range: X: {min(xs)} to {max(xs)}, Y: {min(ys)} to {max(ys)}")
        else:
            print("Pedestrian red not found")

if __name__ == '__main__':
    locate_other_pixels()
