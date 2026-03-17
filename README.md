# Bomberman 2D Game

A fun, fast-paced 2D Bomberman game built with Python and Pygame. Battle against AI opponents or other players in exciting multiplayer modes!

## Features

✨ **Core Gameplay**
- Player characters with smooth animations (12 sprites per character)
- Destructible walls and obstacles
- Bomb placement and explosions with directional spread
- Collision detection and movement physics
- Progressive difficulty levels (3 maps)

⚡ **Power-ups** 
- Bomb Range Extension (+1 range)
- Speed Boost (3-second acceleration)
- Multi-Bomb (place multiple bombs simultaneously)
- Temporary Invincibility (4-second protection)

🎮 **Game Modes**
- **vs Computer**: Challenge the AI opponent (3 difficulty levels based on game progression)
- **Local Multiplayer**: Play with a friend on the same computer (Player 1: Arrows + SPACE, Player 2: WASD + E)
- **Network Multiplayer**: LAN support for playing over network (foundation ready for expansion)

🎯 **Competitive Features**
- 3-lives system per player
- Player name display above characters
- Lives counter in HUD
- Winner detection and victory screen
- Auto-respawn with invincibility period on death

## Installation

### Requirements
- Python 3.8 or higher
- Pygame 2.0+

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bomberman-2d.git
   cd bomberman-2d
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install pygame
   ```

## Running the Game

### From Source
```bash
cd bomberman_2d
python main.py
```

### From Executable (Windows)
1. Download `Bomberman.exe` from the releases page
2. Double-click to run (no installation needed)

## Building the Executable

### Windows (PowerShell)
```powershell
.\build.ps1
```

This will create `dist/Bomberman.exe`

### Manual Build with PyInstaller
```bash
pip install pyinstaller
pyinstaller Bomberman.spec
```

## Game Controls

### Player 1 (Blue)
- **Arrow Keys**: Move
- **SPACE**: Place bomb
- **R**: Restart game
- **ESC**: Quit

### Player 2 (Red) - Local Multiplayer Only
- **WASD**: Move
- **E**: Place bomb
- **R**: Restart game
- **ESC**: Quit

## Game Rules

1. **Objective**: Defeat all opponents by hitting them with bombs
2. **Movement**: Navigate the grid using arrow keys
3. **Bombs**: Place bombs to destroy walls and hit opponents
4. **Power-ups**: Collect items dropped from destroyed walls to gain advantages
5. **Lives**: Each player has 3 lives. Lose all lives = Game Over
6. **Win Condition**: Last player standing with lives remaining wins!

## Game Map

- **13×11 grid** with 40×40 pixel tiles
- **Fixed walls**: Indestructible obstacles (purple)
- **Destructible walls**: Brown blocks that can be cleared with bombs
- **Empty spaces**: Safe areas for movement and bomb placement
- **Exit door**: Appears when all destructible walls are cleared

## Technical Details

### Architecture
- **Tile-based movement system** with collision detection
- **Frame-based animation** (3 frames per direction)
- **Cooldown-based movement** for precise control
- **Bomb timer system** with smooth visual pulsing
- **Event-driven input handling** for responsive controls

### Project Structure
```
bomberman-2d/
├── bomberman_2d/
│   ├── main.py           # Main game file
│   ├── sprites/          # PNG sprite assets
│   └── icon.ico          # Game icon
├── build.ps1             # Build script for .exe
├── Bomberman.spec        # PyInstaller configuration
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

### Game Loop
- 60 FPS rendering
- Event processing (input, collisions)
- Game state updates (animation, timers)
- Rendering to screen

## Performance & Compatibility

- **Tested on**: Windows 10/11
- **Python versions**: 3.8+
- **Minimum specs**: Any modern computer (2GHz CPU, 512MB RAM)
- **File size**: ~30-50MB (packaged executable)

## Power-up Details

| Power-up | Effect | Duration |
|----------|--------|----------|
| 🟨 Bomb Range | +1 bomb explosion range | Permanent |
| 🟩 Speed Boost | Faster movement | 3 seconds |
| 🟪 Multi-Bomb | +1 simultaneous bomb | Permanent |
| ⚪ Invincibility | Temporary protection | 4 seconds |

## Future Enhancements

- [ ] Full network multiplayer support (socket integration)
- [ ] Additional game maps
- [ ] Special abilities per character
- [ ] Sound effects and music
- [ ] High score tracking
- [ ] Customizable controls
- [ ] Different game modes (time limit, item-only, etc.)

## Troubleshooting

**Game won't start**
- Ensure Pygame is installed: `pip install pygame`
- Check Python version: `python --version`

**Sprites not loading**
- Verify `bomberman_2d/sprites/` directory exists with PNG files
- Game has fallback colored shapes if sprites are missing

**Controls not responsive**
- Click on the game window to ensure focus
- Check your keyboard layout settings

## Credits

- Built with [Pygame](https://www.pygame.org/)
- Inspired by the classic Bomberman arcade game
- Python 3.11.9

## License

This project is open source and available under the MIT License.

## Support

For issues, suggestions, or contributions:
1. Create an issue on GitHub
2. Submit a pull request with improvements
3. Share feedback and feature requests

---

**Happy bombing! 💣**

Last Updated: March 17, 2026
