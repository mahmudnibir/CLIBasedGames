import curses
import time
import random

# Game configuration
MAP_WIDTH = 40
MAP_HEIGHT = 20

# Define tile symbols
WALL = "#"
FLOOR = "."
PLAYER_CHAR = "@"
TREASURE = "T"
TRAP = "X"
ENEMY_CHAR = "E"
EXIT = "O"

# Color pair IDs
COLOR_DEFAULT = 1
COLOR_PLAYER = 2
COLOR_WALL = 3
COLOR_FLOOR = 4
COLOR_TREASURE = 5
COLOR_TRAP = 6
COLOR_ENEMY = 7
COLOR_EXIT = 8

def init_colors():
    curses.init_pair(COLOR_DEFAULT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_PLAYER, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_WALL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_FLOOR, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(COLOR_TREASURE, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_TRAP, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_ENEMY, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(COLOR_EXIT, curses.COLOR_CYAN, curses.COLOR_BLACK)

def generate_map():
    game_map = [[FLOOR for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    # Build borders
    for x in range(MAP_WIDTH):
        game_map[0][x] = WALL
        game_map[MAP_HEIGHT - 1][x] = WALL
    for y in range(MAP_HEIGHT):
        game_map[y][0] = WALL
        game_map[y][MAP_WIDTH - 1] = WALL

    # Random walls
    for _ in range(100):
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)
        game_map[y][x] = WALL

    # Random treasures
    for _ in range(10):
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)
        if game_map[y][x] == FLOOR:
            game_map[y][x] = TREASURE

    # Random traps
    for _ in range(8):
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)
        if game_map[y][x] == FLOOR:
            game_map[y][x] = TRAP

    # Random enemies
    for _ in range(6):
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)
        if game_map[y][x] == FLOOR:
            game_map[y][x] = ENEMY_CHAR

    # Place exit in bottom right quadrant
    exit_placed = False
    while not exit_placed:
        x = random.randint(MAP_WIDTH//2, MAP_WIDTH - 2)
        y = random.randint(MAP_HEIGHT//2, MAP_HEIGHT - 2)
        if game_map[y][x] == FLOOR:
            game_map[y][x] = EXIT
            exit_placed = True

    return game_map

# Player class with movement and stats
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.gold = 0
        self.inventory = {"potion": 2}

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            if game_map[new_y][new_x] != WALL:
                self.x = new_x
                self.y = new_y

# Enemy class with basic AI (they wander randomly)
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = random.randint(20, 40)

    def move_random(self, game_map):
        # Try to move in a random direction (only on FLOOR)
        dirs = [(0,1), (0,-1), (1,0), (-1,0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 < new_x < MAP_WIDTH-1 and 0 < new_y < MAP_HEIGHT-1:
                if game_map[new_y][new_x] == FLOOR:
                    self.x = new_x
                    self.y = new_y
                    break

def draw_map(stdscr, game_map, player, enemies):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            ch = game_map[y][x]
            color = COLOR_DEFAULT
            if ch == WALL:
                color = COLOR_WALL
            elif ch == FLOOR:
                color = COLOR_FLOOR
            elif ch == TREASURE:
                color = COLOR_TREASURE
            elif ch == TRAP:
                color = COLOR_TRAP
            elif ch == EXIT:
                color = COLOR_EXIT
            stdscr.addch(y+2, x, ch, curses.color_pair(color))
    # Draw enemies
    for enemy in enemies:
        stdscr.addch(enemy.y+2, enemy.x, ENEMY_CHAR, curses.color_pair(COLOR_ENEMY))
    # Draw player
    stdscr.addch(player.y+2, player.x, PLAYER_CHAR, curses.color_pair(COLOR_PLAYER))

def update_status(stdscr, player):
    status = f"HP: {player.hp} | Gold: {player.gold} | Inventory: {player.inventory}"
    stdscr.addstr(0, 0, status, curses.color_pair(COLOR_DEFAULT))
    stdscr.clrtoeol()

def trigger_treasure(player, stdscr):
    gold = random.randint(10, 50)
    player.gold += gold
    stdscr.addstr(MAP_HEIGHT+3, 0, f"You found treasure! Gold +{gold}.", curses.color_pair(COLOR_TREASURE))
    stdscr.refresh()
    time.sleep(1)

def trigger_trap(player, stdscr):
    damage = random.randint(10, 30)
    player.hp -= damage
    stdscr.addstr(MAP_HEIGHT+3, 0, f"Ouch! A trap dealt {damage} damage.", curses.color_pair(COLOR_TRAP))
    stdscr.refresh()
    time.sleep(1)

def battle(player, enemy, stdscr):
    stdscr.addstr(MAP_HEIGHT+3, 0, f"An enemy attacks! [Battle Started]", curses.color_pair(COLOR_ENEMY))
    stdscr.refresh()
    time.sleep(1)
    while enemy.hp > 0 and player.hp > 0:
        # Player attack
        damage = random.randint(10, 20)
        enemy.hp -= damage
        stdscr.addstr(MAP_HEIGHT+4, 0, f"You hit for {damage} damage. Enemy HP: {max(enemy.hp,0)}   ", curses.color_pair(COLOR_PLAYER))
        stdscr.refresh()
        time.sleep(0.8)
        if enemy.hp <= 0:
            break
        # Enemy attack
        enemy_damage = random.randint(5, 15)
        player.hp -= enemy_damage
        stdscr.addstr(MAP_HEIGHT+5, 0, f"Enemy hits you for {enemy_damage} damage. Your HP: {player.hp}   ", curses.color_pair(COLOR_ENEMY))
        stdscr.refresh()
        time.sleep(0.8)
    if player.hp <= 0:
        stdscr.addstr(MAP_HEIGHT+6, 0, "You were defeated! Game Over. Press any key.", curses.color_pair(COLOR_TRAP))
        stdscr.refresh()
        stdscr.getch()
        exit()
    else:
        gold = random.randint(20, 40)
        player.gold += gold
        stdscr.addstr(MAP_HEIGHT+6, 0, f"Enemy defeated! You earn {gold} gold.             ", curses.color_pair(COLOR_TREASURE))
        stdscr.refresh()
        time.sleep(1)

def trigger_exit(player, stdscr):
    stdscr.addstr(MAP_HEIGHT+3, 0, "You found the exit! Escaping...", curses.color_pair(COLOR_EXIT))
    stdscr.refresh()
    time.sleep(2)
    stdscr.addstr(MAP_HEIGHT+4, 0, f"Congrats! You escaped with {player.gold} gold and {player.hp} HP. Press any key.", curses.color_pair(COLOR_EXIT))
    stdscr.refresh()
    stdscr.getch()
    exit()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(150)
    init_colors()

    game_map = generate_map()
    player = Player(1, 1)

    # Initialize enemies based on map positions
    enemies = []
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if game_map[y][x] == ENEMY_CHAR:
                enemies.append(Enemy(x, y))
                # Clear enemy tile from map to avoid duplicate drawing
                game_map[y][x] = FLOOR

    while True:
        stdscr.clear()
        update_status(stdscr, player)
        draw_map(stdscr, game_map, player, enemies)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            player.move(0, -1, game_map)
        elif key == curses.KEY_DOWN:
            player.move(0, 1, game_map)
        elif key == curses.KEY_LEFT:
            player.move(-1, 0, game_map)
        elif key == curses.KEY_RIGHT:
            player.move(1, 0, game_map)
        elif key == ord('q'):
            break

        # Enemy AI: each enemy moves randomly
        for enemy in enemies:
            enemy.move_random(game_map)

        # Check for collisions and events
        current_tile = game_map[player.y][player.x]
        if current_tile == TREASURE:
            trigger_treasure(player, stdscr)
            game_map[player.y][player.x] = FLOOR
        elif current_tile == TRAP:
            trigger_trap(player, stdscr)
            game_map[player.y][player.x] = FLOOR
        elif current_tile == EXIT:
            trigger_exit(player, stdscr)

        # Check for enemy collision (battle trigger)
        for enemy in enemies:
            if enemy.x == player.x and enemy.y == player.y:
                battle(player, enemy, stdscr)
                # Remove enemy after battle
                enemies.remove(enemy)
                break

        # Player death check
        if player.hp <= 0:
            stdscr.addstr(MAP_HEIGHT+3, 0, "You have perished in the dungeon... Game Over. Press any key.", curses.color_pair(COLOR_TRAP))
            stdscr.refresh()
            stdscr.getch()
            break

        time.sleep(0.1)

curses.wrapper(main)
