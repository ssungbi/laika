import os
from PIL import Image, ImageDraw, ImageFont

def draw_grid():
    img_path = 'assets/car_vs_car.png'
    if not os.path.exists(img_path):
        print(f"{img_path} not found")
        return
    img = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Draw horizontal and vertical lines every 100 pixels
    for x in range(0, w, 100):
        draw.line([(x, 0), (x, h)], fill="red", width=2)
        draw.text((x + 5, 5), str(x), fill="red")
        
    for y in range(0, h, 100):
        draw.line([(0, y), (w, y)], fill="red", width=2)
        draw.text((5, y + 5), str(y), fill="red")
        
    out_path = r'C:\Users\SB\.gemini\antigravity-ide\brain\f67f6715-6121-48bf-99e3-c5f879a79bd9\car_vs_car_grid.png'
    img.save(out_path)
    print(f"Saved gridded image to {out_path}")

if __name__ == '__main__':
    draw_grid()
