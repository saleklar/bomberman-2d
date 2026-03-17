import pygame
import sys
import os
import random
import socket
import json
import threading
import time

# Game settings
TILE_SIZE = 40
GRID_WIDTH = 13
GRID_HEIGHT = 11
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
RED = (255, 0, 0)

# Map layouts (0: empty, 1: wall, 2: destructible)
MAP_LEVEL_1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,2,0,2,0,2,0,2,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,2,0,2,0,2,0,2,0,2,0,2,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,2,0,2,0,2,0,2,0,0,1],
    [1,1,1,0,1,0,1,0,1,0,1,1,1],
    [1,0,0,2,0,2,0,2,0,2,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,2,0,2,0,2,0,2,0,2,0,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
]

MAP_LEVEL_2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,2,2,2,2,2,2,2,2,2,0,1],
    [1,2,1,2,1,2,1,2,1,2,1,2,1],
    [1,0,2,0,2,0,2,0,2,0,2,0,1],
    [1,2,1,2,1,2,1,2,1,2,1,2,1],
    [1,0,2,2,2,0,2,2,2,2,2,0,1],
    [1,1,1,2,1,2,1,2,1,2,1,1,1],
    [1,0,2,0,2,0,2,0,2,0,2,0,1],
    [1,2,1,2,1,2,1,2,1,2,1,2,1],
    [1,0,2,2,2,2,0,2,2,2,2,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
]

MAP_LEVEL_3 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,2,0,2,0,2,0,2,0,2,0,1],
    [1,2,1,2,1,2,1,2,1,2,1,2,1],
    [1,0,2,2,2,2,2,2,2,2,2,0,1],
    [1,2,1,2,0,2,1,2,0,2,1,2,1],
    [1,0,2,0,2,0,2,0,2,0,2,0,1],
    [1,2,1,2,1,2,0,2,1,2,1,2,1],
    [1,0,2,2,2,0,2,2,2,2,2,0,1],
    [1,2,1,2,1,2,1,2,1,2,1,2,1],
    [1,0,2,0,2,0,2,0,2,0,2,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
]

MAPS = [MAP_LEVEL_1, MAP_LEVEL_2, MAP_LEVEL_3]


# ===== NETWORK CODE =====
class GameNetwork:
    """Handle LAN networking for multiplayer Bomberman"""
    def __init__(self, is_server=True, host='localhost', port=5555):
        self.is_server = is_server
        self.host = host
        self.port = port
        self.socket = None
        self.client_socket = None
        self.connected = False
        self.message_queue = []
        self.receive_thread = None
        self.lock = threading.Lock()
    
    def start_server(self):
        """Start server and wait for client connection"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            print(f"Server waiting for connection on {self.host}:{self.port}")
            self.client_socket, addr = self.socket.accept()
            print(f"Client connected from {addr}")
            self.connected = True
            self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            self.receive_thread.start()
            return True
        except Exception as e:
            print(f"Server error: {e}")
            return False
    
    def connect_to_server(self, host):
        """Connect to game server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, self.port))
            print(f"Connected to server at {host}:{self.port}")
            self.connected = True
            self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            self.receive_thread.start()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def _receive_messages(self):
        """Receive messages from network (runs in background thread)"""
        while self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if data:
                    with self.lock:
                        self.message_queue.append(data)
                else:
                    self.connected = False
            except:
                self.connected = False
    
    def send_game_state(self, player_data, ai_data, bombs_data):
        """Send game state to other player"""
        try:
            message = json.dumps({
                'type': 'game_state',
                'player': player_data,
                'ai': ai_data,
                'bombs': bombs_data
            })
            if self.is_server and self.client_socket:
                self.client_socket.send(message.encode('utf-8'))
            elif not self.is_server and self.socket:
                self.socket.send(message.encode('utf-8'))
        except:
            pass
    
    def send_input(self, input_data):
        """Send player input to server"""
        try:
            message = json.dumps({
                'type': 'input',
                'input': input_data
            })
            if self.socket:
                self.socket.send(message.encode('utf-8'))
        except:
            pass
    
    def get_messages(self):
        """Get received messages (thread-safe)"""
        with self.lock:
            messages = self.message_queue[:]
            self.message_queue.clear()
        return messages
    
    def close(self):
        """Close network connection"""
        self.connected = False
        try:
            if self.client_socket:
                self.client_socket.close()
            if self.socket:
                self.socket.close()
        except:
            pass


class SpriteAssets:
    """Load individual sprite files per direction, following daisvke/bomberman design"""
    def __init__(self, asset_dir=None):
        if asset_dir is None:
            # Use the assets folder relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            asset_dir = os.path.join(script_dir, 'assets')
        
        self.sprites = {}  # {direction: {frame: Surface}}
        self.directions = ['up', 'down', 'left', 'right']
        self.frames = [0, 1, 2]  # 3 frames per direction
        
        # Try loading individual sprites for each direction
        for direction in self.directions:
            self.sprites[direction] = {}
            for frame_idx in self.frames:
                frame_name = ['0', 'l', 'r'][frame_idx]  # 0, l, r
                filename = os.path.join(asset_dir, f"player-{direction}-{frame_name}.png")
                try:
                    surf = pygame.image.load(filename).convert_alpha()
                    self.sprites[direction][frame_idx] = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
                    print(f"✓ Loaded {direction}-{frame_name}")
                except FileNotFoundError:
                    # Fallback: create colored surface
                    print(f"✗ Missing {direction}-{frame_name}")
                    self.sprites[direction][frame_idx] = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    self.sprites[direction][frame_idx].fill(BLUE)
    
    def get_sprite(self, direction, frame):
        """Get sprite for a direction and frame number"""
        if direction not in self.sprites or frame not in self.sprites[direction]:
            # Return fallback
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill(BLUE)
            return surf
        return self.sprites[direction][frame]

# --- Entities ---
sprite_assets = None  # Will be initialized in main()

class Player:
    def __init__(self, x, y, color=BLUE, is_ai=False, name="Player"):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.helmet_color = (100, 200, 255) if not is_ai else (255, 100, 100)  # Light blue for player, light red for AI
        self.alive = True
        self.lives = 3  # Each player starts with 3 lives
        self.bombs = []
        self.is_ai = is_ai
        self.anim_frame = 0
        self.anim_timer = 0
        self.last_dxdy = (0, 1)  # Default facing down
        self.ai_move_timer = 0
        self.bomb_range = 1
        self.move_timer = 0  # Cooldown between moves (frames)
        self.base_move_speed = 5 if not is_ai else 8  # Base movement speed
        self.move_speed = self.base_move_speed
        self.speed_boost_timer = 0  # Countdown for speed boost effect
        self.max_bombs = 1  # Max bombs that can be placed at once
        self.invincibility_timer = 0  # Countdown for invincibility effect
        self.last_powerup = None  # Track last collected power-up
        self.powerup_timer = 0  # Timer for power-up message display
        self.spawn_x = x  # Store spawn position
        self.spawn_y = y  # Store spawn position
    
    def die(self):
        """Handle player death with lives system"""
        self.lives -= 1
        if self.lives <= 0:
            self.alive = False
        else:
            # Reset position to spawn point and make invincible for a moment
            self.x = self.spawn_x
            self.y = self.spawn_y
            self.invincibility_timer = 120  # 2 seconds of invincibility (60 FPS)
    
    def ai_move(self, game_map, bombs):
        if not self.alive:
            return
        self.ai_move_timer += 1
        if self.ai_move_timer < 15:
            return
        self.ai_move_timer = 0
        # Random movement
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                if game_map[ny][nx] == 0 and not any(b.x == nx and b.y == ny for b in bombs):
                    self.move(dx, dy, game_map, bombs)
                    break
        # Random bomb placement
        if random.random() < 0.05:
            self.place_bomb(bombs)

    def move(self, dx, dy, game_map, bombs):
        # Check movement cooldown
        self.move_timer += 1
        if self.move_timer < self.move_speed:
            return  # Too soon, can't move yet
        
        # Try to move
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            if game_map[ny][nx] == 0 and not any(b.x == nx and b.y == ny for b in bombs):
                self.x, self.y = nx, ny
                self.last_dxdy = (dx, dy)
                self.move_timer = 0  # Reset cooldown on successful move
                self.anim_timer += 1
                if self.anim_timer >= 6:
                    self.anim_timer = 0
                    self.anim_frame = (self.anim_frame + 1) % 3

    def place_bomb(self, bombs):
        # Check if player can place more bombs (max_bombs limit)
        bombs_at_player = [b for b in bombs if b.x == self.x and b.y == self.y]
        if len(bombs_at_player) < self.max_bombs:
            bombs.append(Bomb(self.x, self.y, range=getattr(self, 'bomb_range', 1)))

    def collect_powerup(self, powerups):
        for p in powerups[:]:
            if p.x == self.x and p.y == self.y:
                if p.type == 'bomb_range':
                    self.bomb_range = getattr(self, 'bomb_range', 1) + 1
                    self.last_powerup = 'BOMB RANGE +1'
                    self.powerup_timer = 120  # Display for 2 seconds at 60 FPS
                elif p.type == 'speed_boost':
                    self.speed_boost_timer = 180  # Speed boost for 3 seconds (180 frames)
                    self.move_speed = max(1, self.base_move_speed - 2)  # 2 frames faster
                    self.last_powerup = 'SPEED BOOST!'
                    self.powerup_timer = 120
                elif p.type == 'multi_bomb':
                    self.max_bombs = getattr(self, 'max_bombs', 1) + 1
                    self.last_powerup = f'MULTI BOMB +1 ({self.max_bombs})'
                    self.powerup_timer = 120
                elif p.type == 'invincibility':
                    self.invincibility_timer = 240  # Invincibility for 4 seconds (240 frames)
                    self.last_powerup = 'INVINCIBILITY!'
                    self.powerup_timer = 120
                powerups.remove(p)

    def update(self):
        """Update timers (speed boost countdown, invincibility countdown, etc)"""
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            # When speed boost ends, revert to base speed
            if self.speed_boost_timer == 0:
                self.move_speed = self.base_move_speed
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
        if self.powerup_timer > 0:
            self.powerup_timer -= 1

    def draw(self, surface):
        # Get sprite based on direction and animation frame
        direction_map = {
            (0, -1): 'up',
            (-1, 0): 'left',
            (1, 0): 'right',
            (0, 1): 'down',
        }
        direction = direction_map.get(self.last_dxdy, 'down')
        frame = self.anim_frame % 3
        
        # Get sprite from global sprite assets
        sprite = sprite_assets.get_sprite(direction, frame)
        
        # Apply transparency for invincibility blinking effect
        if self.invincibility_timer > 0:
            # Blink: show/hide based on timer
            if (self.invincibility_timer // 5) % 2 == 0:  # Blink every 5 frames
                sprite = sprite.copy()
                sprite.set_alpha(150)  # Semi-transparent
        
        surface.blit(sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))
        
        # Draw player name above character
        if self.name:
            font_name = pygame.font.Font(None, 20)
            name_text = font_name.render(self.name, True, WHITE)
            name_rect = name_text.get_rect(center=(self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE - 15))
            surface.blit(name_text, name_rect)
        
        # Draw helmet color indicator
        helmet_rect = pygame.Rect(self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 2, 10, 8)
        pygame.draw.rect(surface, self.helmet_color, helmet_rect)
        pygame.draw.rect(surface, BLACK, helmet_rect, 1)  # Black outline
        
        # Draw invincibility aura
        if self.invincibility_timer > 0:
            aura_color = (255, 255, 100) if (self.invincibility_timer // 5) % 2 == 0 else (255, 200, 0)
            pygame.draw.rect(surface, aura_color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

class Bomb:
    def __init__(self, x, y, timer=120, range=1):
        self.x = x
        self.y = y
        self.timer = timer  # frames until explosion
        self.exploded = False
        self.range = range

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.exploded = True

    def draw(self, surface):
        # Draw bomb as a black circle with pulsing effect
        center_x = self.x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.y * TILE_SIZE + TILE_SIZE // 2
        
        # Base radius
        base_radius = TILE_SIZE // 2 - 4
        
        # Simple oscillating pulse using a sine-like pattern
        # Pulse gets faster as timer approaches 0
        elapsed_time = 120 - self.timer  # How much time has passed
        
        # Pulse speed increases over time
        pulse_speed = 2 + (elapsed_time // 30)  # Speed increases every 30 frames
        pulse_cycle = (elapsed_time * pulse_speed) % 40  # 40-frame pulse cycle
        
        # Create a smooth pulse using simple math (0 to 1 and back)
        if pulse_cycle < 20:
            # Expanding phase
            pulse_amount = (pulse_cycle / 20) * 5  # Expand 0 to 5
        else:
            # Contracting phase
            pulse_amount = ((40 - pulse_cycle) / 20) * 5  # Contract 5 to 0
        
        current_radius = base_radius + pulse_amount
        
        # Draw pulsing bomb
        pygame.draw.circle(surface, BLACK, (center_x, center_y), int(current_radius))

    def draw_explosion(self, surface, positions):
        # Draw explosion effect as orange circles
        for pos in positions:
            x, y = pos
            center_x = x * TILE_SIZE + TILE_SIZE // 2
            center_y = y * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(surface, (255, 165, 0), (center_x, center_y), TILE_SIZE // 2 - 2)

    def explode(self, game_map, powerups, players):
        # Explode in 4 directions, destroy destructible walls (2), kill players
        positions = [(self.x, self.y)]
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            for i in range(1, self.range+1):
                nx, ny = self.x + dx*i, self.y + dy*i
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    if game_map[ny][nx] == 1:
                        break  # Stop at solid wall
                    if game_map[ny][nx] == 2:
                        game_map[ny][nx] = 0
                        # Random chance to spawn powerup
                        if random.random() < 0.2:
                            powerups.append(PowerUp(nx, ny))
                        break  # Stop at destructible wall
                    positions.append((nx, ny))
        # Kill players in explosion (unless invincible)
        for p in players:
            if p.alive and (p.x, p.y) in positions:
                if p.invincibility_timer <= 0:  # Only die if not invincible
                    p.die()  # Call die() method to handle lives system
        return positions

class Wall:
    def __init__(self, x, y, destructible=False):
        self.x = x
        self.y = y
        self.destructible = destructible

    def draw(self, surface):
        x_pos = self.x * TILE_SIZE
        y_pos = self.y * TILE_SIZE
        
        if self.destructible:
            # Draw destructible wall as brown with lighter brick
            pygame.draw.rect(surface, (180, 140, 100), (x_pos, y_pos, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, (100, 70, 40), (x_pos, y_pos, TILE_SIZE, TILE_SIZE), 2)
        else:
            # Draw indestructible wall with brick pattern
            pygame.draw.rect(surface, (139, 69, 19), (x_pos, y_pos, TILE_SIZE, TILE_SIZE))  # Brown background
            # Draw brick lines
            pygame.draw.line(surface, (101, 50, 14), (x_pos, y_pos + TILE_SIZE//2), (x_pos + TILE_SIZE, y_pos + TILE_SIZE//2), 2)
            pygame.draw.line(surface, (101, 50, 14), (x_pos + TILE_SIZE//2, y_pos), (x_pos + TILE_SIZE//2, y_pos + TILE_SIZE), 2)

class PowerUp:
    def __init__(self, x, y, type=None):
        self.x = x
        self.y = y
        # Randomly select type if not specified
        if type is None:
            self.type = random.choice(['bomb_range', 'speed_boost', 'multi_bomb', 'invincibility'])
        else:
            self.type = type

    def draw(self, surface):
        center_x = self.x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.y * TILE_SIZE + TILE_SIZE // 2
        
        if self.type == 'bomb_range':
            # Yellow circle for bomb range
            pygame.draw.circle(surface, (255, 255, 0), (center_x, center_y), TILE_SIZE // 4)
        elif self.type == 'speed_boost':
            # Green circle for speed boost
            pygame.draw.circle(surface, (0, 255, 100), (center_x, center_y), TILE_SIZE // 4)
        elif self.type == 'multi_bomb':
            # Purple circle for multi-bomb
            pygame.draw.circle(surface, (200, 100, 255), (center_x, center_y), TILE_SIZE // 4)
        elif self.type == 'invincibility':
            # White circle for invincibility
            pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), TILE_SIZE // 4)

class Exit:
    """Hidden exit that appears when all destructible blocks are cleared"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = False
        self.blink_timer = 0

    def draw(self, surface):
        if self.visible:
            # Blinking door effect
            self.blink_timer += 1
            if (self.blink_timer // 10) % 2 == 0:  # Blink every 10 frames
                # Draw glowing door
                pygame.draw.rect(surface, (0, 255, 255), (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(surface, (0, 100, 200), (self.x * TILE_SIZE + 4, self.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8), 3)
            if self.blink_timer >= 60:
                self.blink_timer = 0

def count_destructible_blocks(game_map):
    """Count remaining destructible blocks"""
    count = 0
    for row in game_map:
        for tile in row:
            if tile == 2:
                count += 1
    return count

def get_walls(game_map):
    walls = []
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 1:
                walls.append(Wall(x, y, destructible=False))
            elif tile == 2:
                walls.append(Wall(x, y, destructible=True))
    return walls

def draw_map(surface, walls):
    for wall in walls:
        wall.draw(surface)

def show_game_mode_menu(screen, clock):
    """Display menu to choose game mode"""
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    
    options = [
        "1. vs Computer",
        "2. Local Multiplayer (Same PC)",
        "3. Network Multiplayer (LAN)"
    ]
    
    selected = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'ai'
                if event.key == pygame.K_2:
                    return 'local'
                if event.key == pygame.K_3:
                    return 'network'
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return ['ai', 'local', 'network'][selected]
        
        screen.fill((16, 120, 48))
        
        title = font_large.render("BOMBERMAN", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        mode_text = font_medium.render("Select Game Mode:", True, WHITE)
        screen.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 150))
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else WHITE
            text = font_medium.render(option, True, color)
            y_pos = 250 + i * 60
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_pos))
        
        pygame.display.flip()
        clock.tick(FPS)

def get_player_names(screen, clock, player_num=1):
    """Get player name via text input"""
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)
    
    player_name = ""
    max_name_length = 20
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(player_name) > 0:
                        return player_name
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < max_name_length:
                    if event.unicode.isprintable():
                        player_name += event.unicode
        
        screen.fill((16, 120, 48))
        
        title = font_large.render(f"PLAYER {player_num} NAME", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        prompt = font_medium.render("Enter your name:", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 200))
        
        name_text = font_large.render(player_name if player_name else "_", True, (255, 255, 100))
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 280))
        
        hint = font_small.render("Press ENTER to confirm", True, (200, 200, 200))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 380))
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('2D Bomberman - Level Quest')
    clock = pygame.time.Clock()
    global sprite_assets
    sprite_assets = SpriteAssets()

    # Show game mode selection menu
    game_mode = show_game_mode_menu(screen, clock)

    # Get player names for multiplayer modes
    player1_name = "Player 1"
    player2_name = "Player 2" if game_mode in ['local', 'network'] else "CPU"
    
    if game_mode in ['local', 'network']:
        player1_name = get_player_names(screen, clock, 1)
        player2_name = get_player_names(screen, clock, 2)

    # Level system
    current_level = 0
    max_level = len(MAPS) - 1
    
    def init_level(level, mode, p1_name="Player 1", p2_name="Player 2"):
        """Initialize a new level based on game mode"""
        level_map = [row[:] for row in MAPS[level]]  # Make a mutable copy
        player = Player(1, 1, color=BLUE, is_ai=False, name=p1_name)  # Blue player
        
        if mode == 'ai':
            # vs Computer: AI opponent
            ai_speed = 15 - (level * 2)  # Level 0: 15, Level 1: 13, Level 2: 11
            ai_speed = max(5, ai_speed)  # Minimum speed of 5
            opponent = Player(GRID_WIDTH-2, GRID_HEIGHT-2, color=(255, 0, 0), is_ai=True, name="CPU")
            opponent.move_speed = ai_speed
        else:
            # vs Human: Second real player
            opponent = Player(GRID_WIDTH-2, GRID_HEIGHT-2, color=(255, 0, 0), is_ai=False, name=p2_name)
        
        bombs = []
        powerups = []
        walls = get_walls(level_map)
        exit_obj = Exit(GRID_WIDTH - 2, 1)
        
        return player, opponent, bombs, powerups, walls, level_map, exit_obj

    player, opponent, bombs, powerups, walls, game_map, exit_obj = init_level(current_level, game_mode, player1_name, player2_name)
    death_counter = 0  # Counter for auto-reset after death
    level_complete = False
    level_complete_timer = 0

    explosion_positions = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.alive:
                        player.place_bomb(bombs)
                # Player 2 bomb (E key) - only in local multiplayer
                if event.key == pygame.K_e and game_mode == 'local':
                    if opponent.alive:
                        opponent.place_bomb(bombs)
                if event.key == pygame.K_r:
                    # Reset game
                    player, opponent, bombs, powerups, walls, game_map, exit_obj = init_level(current_level, game_mode, player1_name, player2_name)
                    explosion_positions = []

        keys = pygame.key.get_pressed()
        
        # Player 1 controls (arrow keys)
        if player.alive:
            if keys[pygame.K_LEFT]:
                player.move(-1, 0, game_map, bombs)
            if keys[pygame.K_RIGHT]:
                player.move(1, 0, game_map, bombs)
            if keys[pygame.K_UP]:
                player.move(0, -1, game_map, bombs)
            if keys[pygame.K_DOWN]:
                player.move(0, 1, game_map, bombs)
            player.collect_powerup(powerups)
        
        # Player 2 controls (WASD) - only in local multiplayer
        if game_mode == 'local' and opponent.alive and not opponent.is_ai:
            if keys[pygame.K_a]:
                opponent.move(-1, 0, game_map, bombs)
            if keys[pygame.K_d]:
                opponent.move(1, 0, game_map, bombs)
            if keys[pygame.K_w]:
                opponent.move(0, -1, game_map, bombs)
            if keys[pygame.K_s]:
                opponent.move(0, 1, game_map, bombs)
            opponent.collect_powerup(powerups)
        elif game_mode == 'ai':
            # AI opponent
            opponent.ai_move(game_map, bombs)
            opponent.collect_powerup(powerups)
        else:
            # Network mode or other
            if opponent.alive:
                opponent.collect_powerup(powerups)
        
        # Update player timers (speed boost, invincibility, etc.)
        player.update()
        opponent.update()

        # Update bombs
        exploded_bombs = []
        for bomb in bombs:
            bomb.update()
            if bomb.exploded:
                exploded_bombs.append(bomb)
        # Explode bombs and update map
        explosion_positions = []
        for bomb in exploded_bombs:
            positions = bomb.explode(game_map, powerups, [player, opponent])
            explosion_positions.extend(positions)
        bombs = [b for b in bombs if not b.exploded]

        # Update walls after explosions
        walls = get_walls(game_map)

        # Check for winner
        if not opponent.alive and opponent.lives <= 0:
            # Player wins!
            screen.fill((16, 120, 48))
            font_large = pygame.font.Font(None, 72)
            font_medium = pygame.font.Font(None, 48)
            
            winner_text = font_large.render("VICTORY!", True, (255, 215, 0))
            winner_name_text = font_medium.render(f"{player.name} Wins!", True, (0, 200, 0))
            restart_text = pygame.font.Font(None, 32).render("Press R to play again or ESC to quit", True, WHITE)
            
            screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(winner_name_text, (SCREEN_WIDTH // 2 - winner_name_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
            
            pygame.display.flip()
            
            # Handle winner screen events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        player, opponent, bombs, powerups, walls, game_map, exit_obj = init_level(current_level, game_mode, player1_name, player2_name)
                        explosion_positions = []
                        death_counter = 0
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            clock.tick(FPS)
            continue
        
        # Auto-reset if player dies but still has lives
        if not player.alive and player.lives > 0:
            # Player has lives remaining, just reset the level
            player, opponent, bombs, powerups, walls, game_map, exit_obj = init_level(current_level, game_mode, player1_name, player2_name)
            explosion_positions = []
            death_counter = 0
        
        # Auto-reset if all players are dead
        if not player.alive and player.lives <= 0:
            death_counter += 1
            
            # Display game over for 2 seconds (120 frames at 60 FPS) then reset
            screen.fill(WHITE)
            draw_map(screen, walls)
            for bomb in bombs:
                bomb.draw(screen)
            for p in powerups:
                p.draw(screen)
            if explosion_positions:
                Bomb(0,0).draw_explosion(screen, explosion_positions)
            if opponent.alive:
                opponent.draw(screen)
            
            # Draw "GAME OVER" message
            font = pygame.font.Font(None, 48)
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = pygame.font.Font(None, 32).render("Restarting...", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
            
            pygame.display.flip()
            
            # Auto-reset after 2 seconds
            if death_counter >= 120:
                current_level = 0
                player, opponent, bombs, powerups, walls, game_map, exit_obj = init_level(current_level, game_mode, player1_name, player2_name)
                explosion_positions = []
                death_counter = 0
        
        # Clear screen with green background
        screen.fill((16, 120, 48))  # Green ground color
        
        draw_map(screen, walls)
        for bomb in bombs:
            bomb.draw(screen)
        for p in powerups:
            p.draw(screen)
        # Draw explosions
        if explosion_positions:
            Bomb(0,0).draw_explosion(screen, explosion_positions)
        if player.alive:
            player.draw(screen)
        if opponent.alive:
            opponent.draw(screen)
        
        # Update and display power-up messages
        if player.powerup_timer > 0:
            player.powerup_timer -= 1
            font = pygame.font.Font(None, 36)
            powerup_text = font.render(player.last_powerup, True, (255, 200, 0))
            # Draw above player
            text_x = player.x * TILE_SIZE + TILE_SIZE // 2 - powerup_text.get_width() // 2
            text_y = player.y * TILE_SIZE - 30
            screen.blit(powerup_text, (text_x, text_y))
        
        # Display game mode and controls
        font_small = pygame.font.Font(None, 24)
        mode_text = ""
        controls_text = ""
        
        if game_mode == 'ai':
            mode_text = "vs COMPUTER"
            controls_text = "P1: Arrow Keys + SPACE"
        elif game_mode == 'local':
            mode_text = "LOCAL MULTIPLAYER"
            controls_text = "P1: Arrow Keys + SPACE | P2: WASD + E"
        elif game_mode == 'network':
            mode_text = "NETWORK MULTIPLAYER"
            controls_text = "Arrow Keys + SPACE"
        
        mode_surf = font_small.render(mode_text, True, (255, 255, 255))
        screen.blit(mode_surf, (10, 10))
        ctrl_surf = font_small.render(controls_text, True, (200, 200, 200))
        screen.blit(ctrl_surf, (10, 35))
        
        # Display lives for each player
        font_lives = pygame.font.Font(None, 24)
        p1_lives_text = font_lives.render(f"{player.name} Lives: {player.lives}", True, (0, 100, 255))
        p2_lives_text = font_lives.render(f"{opponent.name} Lives: {opponent.lives}", True, (255, 0, 0))
        screen.blit(p1_lives_text, (10, SCREEN_HEIGHT - 30))
        screen.blit(p2_lives_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
