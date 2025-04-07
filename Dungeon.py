import time
import random
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.prompt import Prompt
from rich.text import Text

console = Console()

# ---------- UTILITY FUNCTIONS ----------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def animate_text(text, delay=0.03, style="bold cyan"):
    for char in text:
        console.print(char, end="", style=style)
        time.sleep(delay)
    console.print("")

def loading_animation(task_text="Loading...", duration=1.5):
    for _ in track(range(20), description=task_text):
        time.sleep(duration / 20)

def print_ascii_art(art, title=""):
    panel = Panel(art, title=title, border_style="magenta")
    console.print(panel)

# ---------- GAME CLASSES ----------
class Player:
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.attack_power = 15
        self.inventory = {"potion": 2, "shield": 1}
        self.gold = 0

    def show_status(self):
        animate_text(f"[yellow]HP: {self.hp}/{self.max_hp} | Gold: {self.gold} | Inventory: {self.inventory}[/yellow]", delay=0.005)

    def use_item(self):
        if not self.inventory:
            animate_text("[red]Your inventory is empty![/red]")
            return False
        animate_text("[blue]What item would you like to use? (e.g., potion)[/blue]")
        item = Prompt.ask("Item").lower().strip()
        if item in self.inventory and self.inventory[item] > 0:
            if item == "potion":
                heal_amount = random.randint(20, 35)
                self.hp = min(self.max_hp, self.hp + heal_amount)
                animate_text(f"[green]You drank a potion and healed {heal_amount} HP![/green]")
            elif item == "shield":
                animate_text("[green]You brace yourself with a shield. Incoming damage will be reduced this turn![/green]")
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]
            return item
        else:
            animate_text("[red]You don't have that item![/red]")
            return False

class Enemy:
    def __init__(self, name, hp, attack_power, gold_reward):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.gold_reward = gold_reward

    def is_alive(self):
        return self.hp > 0

# ---------- COMBAT SYSTEM ----------
def battle(player, enemy):
    animate_text(f"\n[bold red]A wild {enemy.name} appears![/bold red]")
    loading_animation(f"Engaging {enemy.name}...", 1)
    shield_active = False

    while enemy.is_alive() and player.hp > 0:
        animate_text(f"\nYour HP: {player.hp} | {enemy.name} HP: {enemy.hp}")
        animate_text("Choose your action: [attack] | [defend] | [item]")
        action = Prompt.ask("Action").lower().strip()
        
        if action == "attack":
            # Player attacks enemy
            damage = random.randint(player.attack_power - 5, player.attack_power + 5)
            enemy.hp -= damage
            animate_text(f"[green]You attack {enemy.name} for {damage} damage![/green]")
        elif action == "defend":
            shield_active = True
            animate_text("[blue]You brace for the next attack, reducing incoming damage![/blue]")
        elif action == "item":
            used_item = player.use_item()
            if used_item == "shield":
                shield_active = True
        else:
            animate_text("[red]Invalid action![/red]")
            continue

        # Enemy turn (if still alive)
        if enemy.is_alive():
            enemy_damage = random.randint(enemy.attack_power - 3, enemy.attack_power + 3)
            if shield_active:
                enemy_damage = max(0, enemy_damage - 10)
                animate_text(f"[blue]Your defense reduced the damage![/blue]")
            player.hp -= enemy_damage
            animate_text(f"[red]{enemy.name} attacks you for {enemy_damage} damage![/red]")
            shield_active = False  # Reset shield effect

        time.sleep(0.8)

    if player.hp <= 0:
        animate_text("[bold red]You have been slain! Game Over.[/bold red]")
        exit()
    else:
        animate_text(f"[bold green]You defeated {enemy.name}![/bold green]")
        player.gold += enemy.gold_reward
        animate_text(f"[yellow]You found {enemy.gold_reward} gold. Total Gold: {player.gold}[/yellow]")
        time.sleep(1)

# ---------- ROOM DEFINITIONS & EVENTS ----------
# Each room is a dictionary with keys:
# - description: text to show
# - options: dict of possible next room keys (or special commands)
# - event: a function to call when entering (optional)

def event_trap(player):
    animate_text("[red]You triggered a hidden trap! Spikes pierce the floor...[/red]")
    damage = random.randint(15, 30)
    player.hp -= damage
    animate_text(f"[red]You take {damage} damage![/red]")
    time.sleep(0.8)

def event_healing(player):
    heal_amount = random.randint(15, 25)
    player.hp = min(player.max_hp, player.hp + heal_amount)
    animate_text(f"[green]A mystical aura heals you for {heal_amount} HP![/green]")
    time.sleep(0.8)

def event_puzzle(player):
    animate_text("[blue]A mystical door asks you a riddle:[/blue]")
    animate_text('"I have keys but no locks, space but no rooms. You can enter, but can’t go outside. What am I?"')
    answer = Prompt.ask("Your answer").lower().strip()
    if "keyboard" in answer:
        animate_text("[green]Correct! The door swings open.[/green]")
    else:
        animate_text("[red]Wrong! The door remains shut, and you are forced back.[/red]")
        return False
    return True

def event_treasure(player):
    gold_found = random.randint(20, 50)
    animate_text(f"[yellow]You find a hidden stash and collect {gold_found} gold![/yellow]")
    player.gold += gold_found
    # Chance to find an item
    if random.random() < 0.5:
        item = random.choice(["potion", "shield"])
        animate_text(f"[yellow]You also find a {item}![/yellow]")
        player.inventory[item] = player.inventory.get(item, 0) + 1
    time.sleep(0.8)

def event_enemy(player):
    enemy_types = [
        {"name": "Goblin", "hp": random.randint(25, 35), "attack": random.randint(10, 15), "gold": random.randint(10, 20)},
        {"name": "Skeleton", "hp": random.randint(30, 40), "attack": random.randint(12, 18), "gold": random.randint(15, 25)},
        {"name": "Dark Knight", "hp": random.randint(35, 50), "attack": random.randint(15, 20), "gold": random.randint(20, 30)}
    ]
    enemy_choice = random.choice(enemy_types)
    enemy = Enemy(enemy_choice["name"], enemy_choice["hp"], enemy_choice["attack"], enemy_choice["gold"])
    battle(player, enemy)

# Define a larger dungeon map with branching paths and events.
rooms = {
    "start": {
        "description": "You awaken in a dim dungeon corridor. Flickering torches reveal two passageways.",
        "options": {"left": "trap_room", "right": "puzzle_room"}
    },
    "trap_room": {
        "description": "The corridor narrows. You feel a sense of dread as you proceed.",
        "event": event_trap,
        "options": {"forward": "treasure_room", "back": "start"}
    },
    "puzzle_room": {
        "description": "An ancient door with cryptic runes blocks your way.",
        "event": event_puzzle,
        "options": {"open": "enemy_room", "back": "start"}
    },
    "treasure_room": {
        "description": "A hidden chamber glitters with promise.",
        "event": event_treasure,
        "options": {"forward": "enemy_room", "back": "trap_room"}
    },
    "enemy_room": {
        "description": "A dark hall resonates with ominous sounds. Danger lurks around every corner.",
        "event": event_enemy,
        "options": {"forward": "boss_room", "back": "treasure_room"}
    },
    "boss_room": {
        "description": "You enter a vast cavern where the Dungeon Boss awaits—a towering, infernal golem!",
        "event": lambda player: battle(player, Enemy("Dungeon Golem", 80, 25, 100)),
        "options": {"escape": "exit", "back": "enemy_room"}
    },
    "exit": {
        "description": "A blinding light appears ahead. Freedom is within your grasp.",
        "options": {}
    }
}

# ---------- GAME LOOP ----------
def play_game():
    player = Player()
    current_room = "start"
    animate_text("Welcome, brave adventurer, to [bold yellow]The Ultimate Dungeon Escape[/bold yellow]!")
    time.sleep(1)
    
    while True:
        clear()
        player.show_status()
        room = rooms[current_room]
        panel = Panel(Text(room["description"], justify="center"), title=f"[bold magenta]{current_room.upper()}[/bold magenta]", border_style="bright_blue")
        console.print(panel)
        
        # Execute room event if present
        if "event" in room:
            result = room["event"](player)
            # For puzzles, if result is False, bounce back to start
            if result is False:
                current_room = "start"
                time.sleep(1)
                continue

        if current_room == "exit":
            art = r"""
  ______     ______     ______     __   __     ______    
 /\  ___\   /\  __ \   /\  ___\   /\ "-.\ \   /\  ___\   
 \ \___  \  \ \  __ \  \ \  __\   \ \ \-.  \  \ \___  \  
  \/\_____\  \ \_\ \_\  \ \_____\  \ \_\\"\_\  \/\_____\ 
   \/_____/   \/_/\/_/   \/_____/   \/_/ \/_/   \/_____/ 
            """
            print_ascii_art(art, title="YOU ESCAPED!")
            animate_text("[bold green]🏁 Congratulations! You have escaped the dungeon alive and richer![/bold green]")
            break

        # List available options
        animate_text("\nAvailable actions:")
        for key in room["options"]:
            animate_text(f"👉 {key}", delay=0.02)
        animate_text("Type [bold blue]'inventory'[/bold blue] to check your items.")
        
        choice = Prompt.ask("\nWhat do you do?").lower().strip()
        if choice == "inventory":
            player.show_status()
            time.sleep(1)
            continue

        if choice in room["options"]:
            current_room = room["options"][choice]
        else:
            animate_text("[red]Invalid choice![/red]")
            time.sleep(1)

if __name__ == "__main__":
    play_game()
