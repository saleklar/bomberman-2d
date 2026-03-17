# Bomberman Sprite File Guide

Following the **daisvke/bomberman** design pattern, the game loads individual sprite files per direction and animation frame.

## Sprite File Structure

Create PNG files in the `assets/` folder with this naming convention:

```
assets/
├── player-up-0.png      # Up direction, frame 0 (neutral)
├── player-up-l.png      # Up direction, frame 1 (left lean)
├── player-up-r.png      # Up direction, frame 2 (right lean)
├── player-down-0.png
├── player-down-l.png
├── player-down-r.png
├── player-left-0.png
├── player-left-l.png
├── player-left-r.png
├── player-right-0.png
├── player-right-l.png
└── player-right-r.png
```

## Sprite Frame Naming

For each direction (up, down, left, right):
- **Frame 0 (`-0`)**: Neutral/standing pose
- **Frame 1 (`-l`)**: Leaning left (alternate animation)
- **Frame 2 (`-r`)**: Leaning right (alternate animation)

The 3-frame animation cycles through these frames creating a walking animation effect.

## How It Works

1. **Player.draw()** gets the current direction from movement
2. **SpriteAssets.get_sprite(direction, frame)** loads the appropriate sprite
3. Animation frame cycles every 6 game frames (at 60 FPS = 0.1 seconds per frame)

## File Format & Size

- **Format**: PNG with transparency support (alpha channel)
- **Size**: 16×16 pixels (will be scaled to 40×40 in-game)
- **Transparency**: Use alpha transparency for non-player areas

## Fallback Graphics

If sprite files are not found:
- Player: Blue rectangle
- Bombs: Black circle
- Walls: Brown rectangles with brick pattern
- Explosions: Orange circles

The game will run with these simple colored graphics while you create the actual sprites.

## Example: Creating Bomberman Sprites

If you have a Bomberman sprite sheet or custom sprites, convert them to individual frames:

1. **Export each direction and frame** as a separate 16×16 PNG
2. **Save with the naming pattern** above
3. **Run the game** - sprites will auto-load when available

## Testing

Run the game and check console output:
- ✓ Messages indicate which sprites loaded successfully
- Missing sprites silently use fallback colored graphics
