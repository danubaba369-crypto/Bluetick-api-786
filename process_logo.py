import sys
from PIL import Image

def analyze_logo():
    img_path = "/Users/macbook/.gemini/antigravity/brain/de6bf050-e44c-463f-bfcc-b1a3fe0b70c7/media__1779394190056.png"
    img = Image.open(img_path)
    width, height = img.size
    print(f"Image dimensions: {width}x{height}")
    
    # Let's inspect some pixel values to find the exact colors
    # We will sample pixels from the center of the text "BLUETIK" and the background
    # Text "BLUETIK" is in the middle-left area. Let's sample a grid.
    blue_pixels = []
    white_pixels = []
    bg_pixels = []
    
    for y in range(0, height, 10):
        for x in range(0, width, 10):
            r, g, b, *a = img.getpixel((x, y))
            # If B is significantly larger than R, it's a blue shade
            if b > r + 40 and b > g + 10:
                blue_pixels.append((x, y, (r, g, b)))
            elif r > 240 and g > 240 and b > 240:
                white_pixels.append((x, y, (r, g, b)))
            else:
                bg_pixels.append((x, y, (r, g, b)))
                
    print(f"Found {len(blue_pixels)} blue pixels, {len(white_pixels)} white pixels")
    if blue_pixels:
        print("Sample blue pixel:", blue_pixels[len(blue_pixels)//2])
    if white_pixels:
        print("Sample white pixel:", white_pixels[len(white_pixels)//2])

if __name__ == "__main__":
    analyze_logo()
