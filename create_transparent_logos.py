import os
import shutil
from PIL import Image

def process_logos():
    img_path = "/Users/macbook/.gemini/antigravity/brain/de6bf050-e44c-463f-bfcc-b1a3fe0b70c7/media__1779394190056.png"
    if not os.path.exists(img_path):
        print(f"Error: Base image not found at {img_path}")
        return
        
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    
    # 1. Find all blue pixels to determine bounding boxes
    blue_pixels = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            # Blueness criteria: B is dominant and B is high
            blueness = b - max(r, g)
            if blueness > 25 and b > 100:
                blue_pixels.append((x, y))
                
    if not blue_pixels:
        print("Error: No blue pixels found!")
        return
        
    min_x = min(p[0] for p in blue_pixels)
    max_x = max(p[0] for p in blue_pixels)
    min_y = min(p[1] for p in blue_pixels)
    max_y = max(p[1] for p in blue_pixels)
    
    print(f"Blue pixels bounding box: x=[{min_x}, {max_x}], y=[{min_y}, {max_y}]")
    
    # The badge is on the right side. Let's find badge blue pixels (e.g., x > min_x + 0.65 * (max_x - min_x))
    badge_threshold_x = min_x + int(0.65 * (max_x - min_x))
    badge_pixels = [p for p in blue_pixels if p[0] > badge_threshold_x]
    
    if not badge_pixels:
        print("Error: No badge pixels found on the right!")
        return
        
    min_bx = min(p[0] for p in badge_pixels)
    max_bx = max(p[0] for p in badge_pixels)
    min_by = min(p[1] for p in badge_pixels)
    max_by = max(p[1] for p in badge_pixels)
    
    bx_center = (min_bx + max_bx) / 2.0
    by_center = (min_by + max_by) / 2.0
    badge_radius = max((max_bx - min_bx) / 2.0, (max_by - min_by) / 2.0)
    
    print(f"Badge Center: ({bx_center:.2f}, {by_center:.2f}), Radius: {badge_radius:.2f}")
    
    # Crop box with padding for full logo
    padding = 20
    crop_box = (
        max(0, min_x - padding),
        max(0, min_y - padding),
        min(width, max_x + padding),
        min(height, max_y + padding)
    )
    
    crop_w = crop_box[2] - crop_box[0]
    crop_h = crop_box[3] - crop_box[1]
    print(f"Crop box: {crop_box} (Width: {crop_w}, Height: {crop_h})")
    
    # Create the transparent dark logo (blue text)
    dark_logo = Image.new("RGBA", (crop_w, crop_h))
    # Create the transparent light logo (white text)
    light_logo = Image.new("RGBA", (crop_w, crop_h))
    
    for y in range(crop_box[1], crop_box[3]):
        for x in range(crop_box[0], crop_box[2]):
            out_x = x - crop_box[0]
            out_y = y - crop_box[1]
            
            r, g, b, a = img.getpixel((x, y))
            
            # Check if this pixel is inside the badge circle
            dist_to_badge_center = ((x - bx_center)**2 + (y - by_center)**2)**0.5
            
            # Inside the badge circle (with a tiny margin for clean edges)
            if dist_to_badge_center <= badge_radius + 4:
                blueness = b - max(r, g)
                # Keep original blue pixels, force grey doodles and other non-blues to solid white
                if blueness > 12 and b > 90:
                    dark_logo.putpixel((out_x, out_y), (r, g, b, 255))
                    light_logo.putpixel((out_x, out_y), (r, g, b, 255))
                else:
                    dark_logo.putpixel((out_x, out_y), (255, 255, 255, 255))
                    light_logo.putpixel((out_x, out_y), (255, 255, 255, 255))
            else:
                # Outside the badge, this belongs to either text or background doodles
                blueness = b - max(r, g)
                
                # Determine alpha based on blueness to get beautiful anti-aliased edges
                # Blue pixels will have high alpha, non-blue will have 0 alpha
                if blueness > 15:
                    # Scale alpha from 0 to 255
                    alpha = int(min(255, max(0, (blueness - 15) * 5)))
                    
                    # For dark logo, keep original blue color
                    dark_logo.putpixel((out_x, out_y), (r, g, b, alpha))
                    
                    # For light logo, change the text color to white
                    light_logo.putpixel((out_x, out_y), (255, 255, 255, alpha))
                else:
                    # Fully transparent background
                    dark_logo.putpixel((out_x, out_y), (0, 0, 0, 0))
                    light_logo.putpixel((out_x, out_y), (0, 0, 0, 0))
                    
    # Save full logos to temp paths in brain first
    brain_dir = "/Users/macbook/.gemini/antigravity/brain/de6bf050-e44c-463f-bfcc-b1a3fe0b70c7"
    dark_logo_path = os.path.join(brain_dir, "extracted_logo_dark.png")
    light_logo_path = os.path.join(brain_dir, "extracted_logo_light.png")
    
    dark_logo.save(dark_logo_path, "PNG")
    light_logo.save(light_logo_path, "PNG")
    
    # 2. Extract Sidebar Collapsed Badge (square image centered around the badge)
    badge_padding = 10
    badge_box = (
        max(0, int(bx_center - badge_radius - badge_padding)),
        max(0, int(by_center - badge_radius - badge_padding)),
        min(width, int(bx_center + badge_radius + badge_padding)),
        min(height, int(by_center + badge_radius + badge_padding))
    )
    
    badge_w = badge_box[2] - badge_box[0]
    badge_h = badge_box[3] - badge_box[1]
    print(f"Badge crop box: {badge_box} (Width: {badge_w}, Height: {badge_h})")
    
    badge_logo = Image.new("RGBA", (badge_w, badge_h))
    
    for y in range(badge_box[1], badge_box[3]):
        for x in range(badge_box[0], badge_box[2]):
            out_x = x - badge_box[0]
            out_y = y - badge_box[1]
            
            r, g, b, a = img.getpixel((x, y))
            dist_to_badge_center = ((x - bx_center)**2 + (y - by_center)**2)**0.5
            
            if dist_to_badge_center <= badge_radius:
                blueness = b - max(r, g)
                if blueness > 12 and b > 90:
                    badge_logo.putpixel((out_x, out_y), (r, g, b, 255))
                else:
                    badge_logo.putpixel((out_x, out_y), (255, 255, 255, 255))
            elif dist_to_badge_center <= badge_radius + 4:
                # Blended edge for smooth circular crop
                blueness = b - max(r, g)
                alpha = int(min(255, max(0, (badge_radius + 4 - dist_to_badge_center) * 63)))
                if blueness > 12 and b > 90:
                    badge_logo.putpixel((out_x, out_y), (r, g, b, alpha))
                else:
                    badge_logo.putpixel((out_x, out_y), (255, 255, 255, alpha))
            else:
                # Transparent outside the circle
                badge_logo.putpixel((out_x, out_y), (0, 0, 0, 0))
                
    badge_logo_path = os.path.join(brain_dir, "extracted_badge_logo.png")
    badge_logo.save(badge_logo_path, "PNG")
    
    # Define Target Copy Paths
    targets = {
        "dark": [
            "/Users/macbook/Documents/wapi-bundle-2.1/wapi-api/uploads/attachments/logo_dark.png",
            "/Users/macbook/Documents/wapi-bundle-2.1/Wapi-frontend/public/assets/logos/logo3.png",
            "/Users/macbook/Documents/wapi-bundle-2.1/Wapi-admin/public/assets/logos/logo3.png"
        ],
        "light": [
            "/Users/macbook/Documents/wapi-bundle-2.1/wapi-api/uploads/attachments/logo_light.png",
            "/Users/macbook/Documents/wapi-bundle-2.1/Wapi-frontend/public/assets/logos/logo1.png",
            "/Users/macbook/Documents/wapi-bundle-2.1/Wapi-admin/public/assets/logos/logo1.png"
        ],
        "badge": [
            "/Users/macbook/Documents/wapi-bundle-2.1/wapi-api/uploads/attachments/sidebar_dark_logo.png",
            "/Users/macbook/Documents/wapi-bundle-2.1/wapi-api/uploads/attachments/sidebar_light_logo.png",
            "/Users/macbook/Documents/wapi-bundle-2.1/wapi-api/uploads/attachments/favicon.png",
            "/Users/macbook/Documents/wapi-bundle-2.1/Wapi-frontend/public/assets/logos/sidebarLogo.png",
            "/Users/macbook/Documents/wapi-bundle-2.1/Wapi-admin/public/assets/logos/sidebarLogo.png"
        ]
    }
    
    # Copy generated images to destination directories
    for key, path_list in targets.items():
        src_path = {
            "dark": dark_logo_path,
            "light": light_logo_path,
            "badge": badge_logo_path
        }[key]
        
        for dst_path in path_list:
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print(f"Copied {key} logo to: {dst_path}")
            
    print("\nAll logos successfully generated, cleaned, and copied to targets!")

if __name__ == "__main__":
    process_logos()
