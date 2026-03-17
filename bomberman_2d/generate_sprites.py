"""
Generate simple Bomberman placeholder sprites programmatically.
This creates the required sprite PNG files so the game has visuals.
"""
import os
from PIL import Image, ImageDraw

def create_bomberman_sprite(direction, frame_type):
    """
    Create a simple Bomberman sprite.
    
    direction: 'up', 'down', 'left', 'right'
    frame_type: '0' (neutral), 'l' (left lean), 'r' (right lean)
    """
    # 16x16 pixels with white background
    img = Image.new('RGBA', (16, 16), (0, 200, 0, 0))  # Transparent
    draw = ImageDraw.Draw(img)
    
    # Draw simple Bomberman character
    # Body (red square)
    draw.rectangle([3, 4, 12, 12], fill=(200, 50, 50, 255))
    
    # Head (yellow circle)
    draw.ellipse([4, 1, 11, 8], fill=(255, 200, 0, 255))
    
    # Eyes
    draw.rectangle([5, 3, 6, 4], fill=(0, 0, 0, 255))
    draw.rectangle([9, 3, 10, 4], fill=(0, 0, 0, 255))
    
    # Legs - animate based on frame
    leg_offset = 0
    if frame_type == 'l':
        leg_offset = -1
    elif frame_type == 'r':
        leg_offset = 1
    
    # Left leg
    draw.rectangle([4 + leg_offset, 12, 6 + leg_offset, 14], fill=(100, 50, 200, 255))
    # Right leg
    draw.rectangle([9 - leg_offset, 12, 11 - leg_offset, 14], fill=(100, 50, 200, 255))
    
    # Arms based on direction
    if direction == 'up':
        draw.rectangle([2, 5, 3, 10], fill=(255, 200, 0, 255))  # Left arm
        draw.rectangle([12, 5, 13, 10], fill=(255, 200, 0, 255))  # Right arm
    elif direction == 'down':
        draw.rectangle([2, 6, 3, 11], fill=(255, 200, 0, 255))  # Left arm
        draw.rectangle([12, 6, 13, 11], fill=(255, 200, 0, 255))  # Right arm
    elif direction == 'left':
        draw.rectangle([1, 6, 3, 8], fill=(255, 200, 0, 255))  # Arm pointing left
    elif direction == 'right':
        draw.rectangle([12, 6, 14, 8], fill=(255, 200, 0, 255))  # Arm pointing right
    
    return img

def main():
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    directions = ['up', 'down', 'left', 'right']
    frames = ['0', 'l', 'r']
    
    print("Generating Bomberman sprites...")
    for direction in directions:
        for frame in frames:
            img = create_bomberman_sprite(direction, frame)
            filename = f"player-{direction}-{frame}.png"
            filepath = os.path.join(assets_dir, filename)
            img.save(filepath)
            print(f"✓ Created {filename}")
    
    print(f"\n✅ All sprites created in {assets_dir}/")
    print("Run the game again to see the sprites!")

if __name__ == '__main__':
    main()
