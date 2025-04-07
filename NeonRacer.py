import curses
import time
import random

# --- Game Configuration ---
TRACK_WIDTH = 40        # Width of the game track area
TRACK_HEIGHT = 20       # Height of the game area
BORDER_CHAR = "║"       # Border symbol for the track
SCORE_WIN_HEIGHT = 5    # Space for header/HUD

# Symbols for game elements
PLAYER_CHAR = "➹"       # Your car
OBSTACLE_CHAR = "▣"     # Standard obstacle (block)
ENEMY_CHAR = "V"        # Enemy vehicle (tries to block you)
POWERUP_CHAR = "★"      # Power-up symbol

# Timing and speed settings (milliseconds)
INITIAL_SPEED = 100     # Lower means faster game loop
SPEED_INCREMENT = 2     # Speed up as score increases

# Chance probabilities for new elements in new rows
OBSTACLE_PROB = 0.10    # 10% chance for a standard obstacle
ENEMY_PROB = 0.05       # 5% chance for an enemy vehicle
POWERUP_PROB = 0.03     # 3% chance for a power-up

# --- Color Pair IDs ---
COLOR_PLAYER = 1
COLOR_OBSTACLE = 2
COLOR_ENEMY = 3
COLOR_BORDER = 4
COLOR_BG = 5
COLOR_HUD = 6
COLOR_POWERUP = 7
COLOR_HEADER = 8

def init_colors():
    curses.init_pair(COLOR_PLAYER, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_OBSTACLE, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_ENEMY, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(COLOR_BORDER, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_BG, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(COLOR_HUD, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_POWERUP, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_HEADER, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

def draw_header(header_win, sw):
    header_win.erase()
    logo = [
        " _   _  ______  _   _  _____  _   _  _____   _____  _____  _____ ",
        "| \\ | ||  _  \\| \\ | ||  _  || \\ | ||  _  | /  ___||  _  ||  _  |",
        "|  \\| || | | ||  \\| || | | ||  \\| || | | | \\ `--. | | | || | | |",
        "| . ` || | | || . ` || | | || . ` || | | |  `--. \\| | | || | | |",
        "| |\\  || |/ / | |\\  \\| |/ / | |\\  || |/ /  /\\__/ /\\ \\_/ /\\ \\_/ /",
        "\\_| \\_/|___/  \\_| \\_/|___/  \\_| \\_/|___/   \\____/  \\___/  \\___/ "
    ]
    for idx, line in enumerate(logo):
        x = max((sw - len(line)) // 2, 0)
        header_win.addstr(idx, x, line, curses.color_pair(COLOR_HEADER) | curses.A_BOLD)
    header_win.noutrefresh()

def draw_hud(hud_win, score, combo, active_powerup):
    hud_win.erase()
    powerup_text = f"Power-Up: {active_powerup}" if active_powerup else "Power-Up: None"
    hud_text = f" Score: {score}   Combo: {combo}   {powerup_text}   [Arrows: Move | Q: Quit] "
    hud_win.addstr(0, 0, hud_text, curses.color_pair(COLOR_HUD))
    hud_win.noutrefresh()

def generate_initial_map():
    # Create initial track as a list of rows
    # Each row is a list of characters (including borders)
    game_map = []
    # Top border
    top_row = [BORDER_CHAR] * TRACK_WIDTH
    game_map.append(top_row)
    # Interior rows filled with blank space
    for _ in range(TRACK_HEIGHT - 2):
        row = [" "] * TRACK_WIDTH
        row[0] = BORDER_CHAR
        row[-1] = BORDER_CHAR
        game_map.append(row)
    # Bottom border
    bottom_row = [BORDER_CHAR] * TRACK_WIDTH
    game_map.append(bottom_row)
    return game_map

def add_new_row():
    # Generate a new row with borders and random elements
    new_row = [" "] * TRACK_WIDTH
    new_row[0] = BORDER_CHAR
    new_row[-1] = BORDER_CHAR
    for x in range(1, TRACK_WIDTH - 1):
        r = random.random()
        if r < POWERUP_PROB:
            new_row[x] = POWERUP_CHAR
        elif r < POWERUP_PROB + ENEMY_PROB:
            new_row[x] = ENEMY_CHAR
        elif r < POWERUP_PROB + ENEMY_PROB + OBSTACLE_PROB:
            new_row[x] = OBSTACLE_CHAR
        else:
            new_row[x] = " "
    return new_row

# --- Player Class ---
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100  # Could be used for extended mechanics
        self.active_powerup = None  # e.g., "Shield", "Slow Time"
        self.powerup_timer = 0

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        # Prevent moving into borders
        if 0 < new_x < TRACK_WIDTH - 1 and 0 < new_y < TRACK_HEIGHT - 1:
            self.x = new_x
            self.y = new_y

    def update_powerup(self):
        if self.active_powerup:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.active_powerup = None

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(INITIAL_SPEED)
    init_colors()

    sh, sw = stdscr.getmaxyx()
    # Check for minimum terminal size
    if sh < 32 or sw < 60:
        stdscr.addstr(0, 0, "Terminal too small! Resize to at least 60x32 and try again.")
        stdscr.refresh()
        stdscr.getch()
        return

    # Create windows: header, HUD, and game area
    header_win = curses.newwin(7, sw, 0, 0)
    hud_win = curses.newwin(1, sw, 7, 0)
    game_win = curses.newwin(TRACK_HEIGHT, TRACK_WIDTH, SCORE_WIN_HEIGHT + 7, (sw - TRACK_WIDTH) // 2)
    game_win.keypad(True)
    
    # Initialize track map and player
    game_map = generate_initial_map()
    player = Player(TRACK_WIDTH // 2, TRACK_HEIGHT - 2)
    
    score = 0
    combo = 0
    speed = INITIAL_SPEED
    frame = 0

    # Main Game Loop
    while True:
        stdscr.erase()
        draw_header(header_win, sw)
        draw_hud(hud_win, score, combo, player.active_powerup)

        # Draw game window border with color
        game_win.border(BORDER_CHAR, BORDER_CHAR, BORDER_CHAR, BORDER_CHAR)
        # Draw game map
        for y in range(1, TRACK_HEIGHT - 1):
            for x in range(1, TRACK_WIDTH - 1):
                ch = game_map[y][x]
                if ch == OBSTACLE_CHAR:
                    color = COLOR_OBSTACLE
                elif ch == ENEMY_CHAR:
                    color = COLOR_ENEMY
                elif ch == POWERUP_CHAR:
                    color = COLOR_POWERUP
                else:
                    color = COLOR_BG
                game_win.addch(y, x, ch, curses.color_pair(color))
        # Draw player
        game_win.addch(player.y, player.x, PLAYER_CHAR, curses.color_pair(COLOR_PLAYER) | curses.A_BOLD)
        
        game_win.noutrefresh()
        curses.doupdate()

        # Handle user input
        key = game_win.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_LEFT:
            player.move(-1, 0, game_map)
        elif key == curses.KEY_RIGHT:
            player.move(1, 0, game_map)
        elif key == curses.KEY_UP:
            player.move(0, -1, game_map)
        elif key == curses.KEY_DOWN:
            player.move(0, 1, game_map)

        # Scroll the track: add a new row at the top and remove the bottom row
        new_row = add_new_row()
        game_map.pop()          # Remove bottom row
        game_map.insert(1, new_row)  # Insert new row just below top border

        # Check for collisions at player's position in the new map row:
        current_tile = game_map[player.y][player.x]
        if current_tile in [OBSTACLE_CHAR, ENEMY_CHAR]:
            # If player has an active shield power-up, negate collision
            if player.active_powerup == "Shield":
                combo += 1  # Increase combo bonus instead of penalty
            else:
                stdscr.addstr(sh//2, (sw - 20)//2, "  GAME OVER  ", curses.color_pair(COLOR_OBSTACLE) | curses.A_BOLD)
                stdscr.refresh()
                stdscr.nodelay(False)
                stdscr.getch()
                break
        elif current_tile == POWERUP_CHAR:
            # Activate a power-up: Shield lasts for a fixed number of frames
            player.active_powerup = "Shield"
            player.powerup_timer = 50
            combo += 5  # Bonus for collecting a power-up
            # Clear the power-up from the map so it isn't collected repeatedly
            game_map[player.y][player.x] = " "

        score += 1
        player.update_powerup()

        # Increase speed (i.e., decrease timeout) as score increases, up to a limit
        if score % 100 == 0 and speed > 20:
            speed -= SPEED_INCREMENT
            stdscr.timeout(speed)

        time.sleep(0.05)
        frame += 1

curses.wrapper(main)
