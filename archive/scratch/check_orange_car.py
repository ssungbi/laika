import os
from PIL import Image

def crop_and_check():
    img_path = 'assets/car_vs_car.png'
    if not os.path.exists(img_path):
        print(f"{img_path} not found")
        return
    img = Image.open(img_path)
    
    # Bounding box of orange car: 280, 219, 526, 650
    crop_box = (280, 219, 526, 650)
    cropped = img.crop(crop_box)
    
    out_path = r'C:\Users\SB\.gemini\antigravity-ide\brain\f67f6715-6121-48bf-99e3-c5f879a79bd9\orange_car_crop.png'
    cropped.save(out_path)
    print(f"Saved orange car crop to {out_path}")

if __name__ == '__main__':
    crop_and_check()
