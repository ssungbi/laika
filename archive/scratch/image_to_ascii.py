import os
from PIL import Image

def image_to_ascii():
    img_path = 'assets/car_vs_car.png'
    if not os.path.exists(img_path):
        print(f"{img_path} not found")
        return
    img = Image.open(img_path).convert('RGB')
    # Resize to 80x40 for clean terminal display
    w, h = 80, 40
    img = img.resize((w, h), Image.Resampling.NEAREST)
    
    # We will map colors to characters
    # C: Orange/Blue Cars
    # T: Green Trees
    # B: Brown Buildings
    # R: Grey Road
    # .: Background/Sky
    
    for y in range(h):
        line = ""
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            # Detect green tree
            if g > r + 30 and g > b + 30:
                line += "T"
            # Detect orange car
            elif r > 180 and g > 80 and g < 160 and b < 80:
                line += "O"
            # Detect blue/teal car
            elif b > 150 and g > 100 and r < 80:
                line += "U"
            # Detect brown building
            elif r > 100 and g > 60 and g < 130 and b < 100:
                line += "B"
            # Detect grey road
            elif abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15 and r > 80 and r < 180:
                line += "R"
            else:
                line += "."
        print(line)

if __name__ == '__main__':
    image_to_ascii()
