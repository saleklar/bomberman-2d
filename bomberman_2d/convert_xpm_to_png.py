"""
Convert XPM sprites from the reference Bomberman project to PNG format.
This extracts player and enemy sprites and saves them as PNG files.
"""
import os
from PIL import Image

def parse_xpm(xpm_path):
    """Parse an XPM file and return a PIL Image."""
    with open(xpm_path, 'r') as f:
        lines = f.readlines()
    
    # Find header line with width, height, colors, chars_per_pixel
    header_line = None
    pixel_start = None
    
    for i, line in enumerate(lines):
        if 'columns rows colors' in line:
            header_line = i + 1
            break
    
    if header_line is None:
        print(f"Could not parse {xpm_path}")
        return None
    
    # Parse dimensions
    dims_line = lines[header_line].strip().strip('",')
    width, height, colors, cpp = map(int, dims_line.split())
    
    # Build color map
    color_map = {}
    i = header_line + 1
    for _ in range(colors):
        line = lines[i].strip()
        if line.endswith(',') or line.endswith('};'):
            line = line[:-1]
        line = line.strip('"')
        
        # Parse color definition: "X c #RRGGBB"
        char = line[0]
        color_str = line.split('#')[-1] if '#' in line else 'FFFFFF'
        
        try:
            r = int(color_str[0:2], 16)
            g = int(color_str[2:4], 16)
            b = int(color_str[4:6], 16)
            color_map[char] = (r, g, b, 255)
        except:
            color_map[char] = (200, 200, 200, 255)  # Default gray
        
        i += 1
    
    # Find pixels section
    pixel_start = i
    
    # Create image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()
    
    # Parse pixel data
    y = 0
    for line_idx in range(pixel_start, len(lines)):
        line = lines[line_idx].strip()
        if line.startswith('"') and not line.startswith('"*'):
            line = line.strip('",')
            for x, char in enumerate(line):
                if x < width and y < height:
                    pixels[x, y] = color_map.get(char, (200, 200, 200, 255))
            y += 1
            if y >= height:
                break
    
    return img

def convert_sprites():
    """Convert XPM sprites to PNG and save to assets folder."""
    ref_img_dir = "E:\\VIBE_PROJECTS\\bomberman test\\bomberman_reference\\img"
    asset_dir = os.path.join(os.path.dirname(__file__), 'assets')
    os.makedirs(asset_dir, exist_ok=True)
    
    # Mapping of XPM files to PNG names for our game
    sprite_mappings = {
        # Player sprites (white characters)
        'white-up-0.xpm': 'player-up-0.png',
        'white-up-l.xpm': 'player-up-l.png',
        'white-up-r.xpm': 'player-up-r.png',
        'white-down-0.xpm': 'player-down-0.png',
        'white-down-l.xpm': 'player-down-l.png',
        'white-down-r.xpm': 'player-down-r.png',
        'white-left-0.xpm': 'player-left-0.png',
        'white-left-l.xpm': 'player-left-l.png',
        'white-left-r.xpm': 'player-left-r.png',
        'white-right-0.xpm': 'player-right-0.png',
        'white-right-l.xpm': 'player-right-l.png',
        'white-right-r.xpm': 'player-right-r.png',
    }
    
    print("Converting XPM sprites to PNG...")
    for xpm_name, png_name in sprite_mappings.items():
        xpm_path = os.path.join(ref_img_dir, xpm_name)
        png_path = os.path.join(asset_dir, png_name)
        
        if not os.path.exists(xpm_path):
            print(f"⚠ Not found: {xpm_name}")
            continue
        
        try:
            img = parse_xpm(xpm_path)
            if img:
                # Scale to 16x16 (original XPM is 24x24)
                img_scaled = img.resize((16, 16), Image.Resampling.LANCZOS)
                img_scaled.save(png_path)
                print(f"✓ {png_name}")
            else:
                print(f"✗ Failed to parse {xpm_name}")
        except Exception as e:
            print(f"✗ Error converting {xpm_name}: {e}")
    
    print(f"\n✅ Sprites converted to {asset_dir}/")

if __name__ == '__main__':
    convert_sprites()
