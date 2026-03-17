# 🎮 Bomberman 2D - A Modern Pygame Implementation

A fully-featured 2D Bomberman game built with Python and Pygame, featuring AI opponents, local multiplayer, network support, and progressive level system.

## Features

### 🎯 Gameplay
- **3 Game Modes:**
  - vs Computer AI (progressively harder)
  - Local Multiplayer (same computer, 2 players)
  - Network Multiplayer (LAN support)
- **Progressive Levels** - 3 different maze layouts with increasing difficulty
- **Power-ups:**
  - 💛 Bomb Range (+1)
  - 🟢 Speed Boost (3 seconds)
  - 🟣 Multi-Bomb (place more bombs)
  - ⚪ Invincibility (4 seconds)
- **Dynamic Bomb Pulsing** - Bombs grow larger and pulse faster as they approach detonation
- **Real Bomberman Sprites** - 12 animation frames per character (4 directions × 3 frames)
- **Death & Respawn** - Auto-reset on death with 2-second countdown

### 🎨 Visual Polish
- Professional sprite graphics (converted from XPM format)
- Helmet color distinction (blue for player, red for opponent)
- Invincibility visual effects (golden aura + transparency blinking)
- Animated wall destruction
- Smooth explosion effects

### 🤖 AI Features
- Intelligent random pathfinding
- Adaptive bomb placement
- Level-based difficulty scaling
- Speed increases with each level

### 🕹️ Controls

#### vs Computer / Network Mode
- `Arrow Keys` - Move
- `SPACE` - Place bomb
- `R` - Reset game

#### Local Multiplayer
- **Player 1 (Blue):** Arrow Keys to move, SPACE to place bomb
- **Player 2 (Red):** WASD to move, E to place bomb

## Installation

### Requirements
- Python 3.7+
- Pygame 2.0+

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bomberman-2d.git
   cd bomberman-2d/bomberman_2d
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install pygame
   ```

4. **Run the game:**
   ```bash
   python main.py
   ```

## How to Play

1. Start the game - you'll see a menu with 3 options
2. Choose your game mode (1, 2, 3 or use arrow keys)
3. Control your character and eliminate your opponent
4. Destroy blocks to find power-ups and open the path to the exit
5. Reach the exit to advance to the next level

## Game Mechanics

- **Walls:** 
  - Brown walls: Indestructible
  - Light brown: Destructible (destroyed by explosions)
- **Bombs:** 
  - Explode after ~2 seconds
  - Pulse effect indicates detonation time
  - Destroy blocks and kill players in 4-direction paths
- **Power-ups:** Randomly spawn from destroyed blocks (20% chance)

## Building as Executable

To package the game as a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "assets:assets" main.py
```

The executable will be in the `dist/` folder.

## Project Structure

```
bomberman_2d/
├── main.py                 # Main game file
├── assets/                 # Sprite assets
│   ├── player-up-*.png
│   ├── player-down-*.png
│   ├── player-left-*.png
│   └── player-right-*.png
├── convert_xpm_to_png.py  # Sprite conversion utility
├── .gitignore
└── README.md
```

## Roadmap

- [ ] Complete LAN multiplayer sync
- [ ] Boss/villain character for final level
- [ ] Sound effects and background music
- [ ] Additional power-up types
- [ ] Leaderboard system
- [ ] Mobile/mobile web version

## Technical Details

### Architecture
- **Tile-based grid system** (13×11 tiles, 40px per tile)
- **Event-driven input** with Movement cooldown system
- **Frame-based timing** (60 FPS)
- **Sprite animation** (3-frame cycles per direction)
- **Network code** (socket-based, ready for enhancement)

### Game Classes
- `SpriteAssets` - Sprite loading and management
- `Player` - Player/AI character with movement and animation
- `Bomb` - Bomb logic with pulsing effect and explosion
- `Wall` - Destructible and indestructible walls
- `PowerUp` - Power-up system with randomization
- `Exit` - Hidden exit door (appears when all blocks cleared)
- `GameNetwork` - LAN networking infrastructure

## Performance

- Runs at **60 FPS** consistently
- Sprite fallback system (colored rectangles if assets missing)
- Optimized collision detection
- Efficient explosion calculation

## Known Issues

- Network multiplayer requires manual sync implementation
- Asset files needed for full sprite display (graceful fallback to colored shapes)

## License

MIT License - Feel free to use, modify, and distribute

## Credits

- Sprite design based on [daisvke/bomberman](https://github.com/daisvke/bomberman)
- Built with [Pygame](https://www.pygame.org)
- Game concept from classic Bomberman

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

**Made with ❤️ using Python & Pygame**
