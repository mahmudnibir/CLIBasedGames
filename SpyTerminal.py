#!/usr/bin/env python3
import os
import time
import threading
import random
import sys

# ANSI color codes for optional theming
class Colors:
    HEADER   = "\033[95m"
    BLUE     = "\033[94m"
    CYAN     = "\033[96m"
    GREEN    = "\033[92m"
    WARNING  = "\033[93m"
    RED      = "\033[91m"
    ENDC     = "\033[0m"

# Animated ASCII text effects for narrative and transitions
def animate_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def ascii_animation(frames, frame_delay=0.3, repeat=1):
    for _ in range(repeat):
        for frame in frames:
            os.system('cls' if os.name=='nt' else 'clear')
            print(frame)
            time.sleep(frame_delay)

# ASCII animations for key events
MISSION_START_ANIMATION = [
    Colors.HEADER + r"""
   _______ _            _______        _       
  |__   __| |          |__   __|      | |      
     | |  | |__   ___     | | ___  ___| |_ ___ 
     | |  | '_ \ / _ \    | |/ _ \/ __| __/ __|
     | |  | | | |  __/    | |  __/\__ \ |_\__ \
     |_|  |_| |_|\___|    |_|\___||___/\__|___/
    """ + Colors.ENDC,
    Colors.HEADER + r"""
    _____ _           _      _       
   / ____| |         (_)    | |      
  | |    | |__   __ _ _ _ __| |_ ___ 
  | |    | '_ \ / _` | | '__| __/ __|
  | |____| | | | (_| | | |  | |_\__ \
   \_____|_| |_|\__,_|_|_|   \__|___/
    """ + Colors.ENDC,
]

BOMB_WARNING_FRAMES = [
    Colors.RED + r"""
     ___________
    |  BOOM!!!  |
    |  #######  |
    |  #######  |
    |  #######  |
    |___________|
    """ + Colors.ENDC,
    Colors.RED + r"""
     ___________
    |  BOOM!!!  |
    |   #####   |
    |  #######  |
    |   #####   |
    |___________|
    """ + Colors.ENDC,
]

# Simulated file/directory node for our virtual file system
class FSNode:
    def __init__(self, name, node_type="dir", content="", children=None):
        self.name = name
        self.type = node_type  # 'dir' or 'file'
        self.content = content
        self.children = children if children is not None else {}
    
    def add_child(self, child):
        if self.type != "dir":
            raise ValueError("Files cannot contain children!")
        self.children[child.name] = child

# Our dynamic file system built like a digital dossier
class FileSystem:
    def __init__(self):
        self.root = FSNode("root")
        self.populate_fs()
    
    def populate_fs(self):
        # Mission Brief folder
        missions = FSNode("missions")
        mission_brief = FSNode("brief.txt", "file", 
            "Agent,\n\n"
            "Welcome to Operation NIGHTSHADE. Your objective is twofold:\n"
            "  1. Retrieve the classified intel hidden deep within the digital archives.\n"
            "  2. Defuse the enemy's ticking time bomb before it detonates.\n\n"
            "Instructions:\n"
            "  - Navigate the file system using 'cd' to enter directories and 'ls' to list files.\n"
            "  - Read files with 'cat' to gather clues. For example, 'cat brief.txt'.\n"
            "  - The intel is stored in the 'intel' directory. Find and read 'classified.txt'.\n"
            "  - After acquiring intel, enter the 'bomb_module' directory, arm the bomb with 'arm_bomb', then defuse it with 'defuse 1-4-1'.\n\n"
            "Time is of the essence, Agent. Trust no one and watch your back.\n"
            "Good luck.\n"
        )
        missions.add_child(mission_brief)
        
        # Classified Intel folder
        intel = FSNode("intel")
        classified = FSNode("classified.txt", "file",
            "TOP SECRET\n\n"
            "The enemy's plan is underway. The disarm code is concealed within the command history.\n"
            "Remember: Clues can be found in the errors and logs...\n"
            "You might want to review everything with 'history' and 'grep'.\n\n"
            "Hint: The code format is digit-digit-digit, where the digits sum to 6.\n"
            "Hint: Look closely, Agent...\n"
        )
        intel.add_child(classified)
        
        # Bomb Module folder
        bomb_module = FSNode("bomb_module")
        bomb_instr = FSNode("instructions.txt", "file",
            "WARNING: Bomb ACTIVE\n\n"
            "This module contains the device set to obliterate our network.\n"
            "To proceed, you must arm the bomb by using the command 'arm_bomb'.\n"
            "Immediately after, decipher the clues and enter the correct code to defuse with 'defuse [code]'.\n\n"
            "Clue: The code is hidden in plain sight. Trust the intel.\n"
        )
        bomb_module.add_child(bomb_instr)
        
        # System Logs folder
        logs = FSNode("logs")
        system_log = FSNode("system.log", "file",
            "[00:01] Intrusion detected at perimeter.\n"
            "[00:05] Agent access granted; mission initiated.\n"
            "[00:10] Bomb module engaged, threat level critical.\n"
            "[00:15] Classified intel retrieved from secure server.\n"
        )
        logs.add_child(system_log)
        
        # Add all to root
        self.root.add_child(missions)
        self.root.add_child(intel)
        self.root.add_child(bomb_module)
        self.root.add_child(logs)
    
    def get_node(self, path_list):
        current = self.root
        if not path_list or path_list[0] == "":
            return current
        for part in path_list:
            if part in current.children:
                current = current.children[part]
            else:
                return None
        return current

# Bomb mechanism with integrated visual warnings and puzzle logic.
class Bomb:
    def __init__(self, countdown=30):
        self.countdown = countdown  # Total seconds to defuse
        self.timer_thread = None
        self.defused = False
    
    def start_countdown(self):
        print(Colors.RED + "\n*** ALERT: Bomb Activated ***" + Colors.ENDC)
        self.timer_thread = threading.Thread(target=self._run_countdown)
        self.timer_thread.start()
    
    def _run_countdown(self):
        start_time = time.time()
        while time.time() - start_time < self.countdown:
            if self.defused:
                print(Colors.GREEN + f"\nBomb defused with {int(self.countdown - (time.time() - start_time))} sec remaining!" + Colors.ENDC)
                return
            time_left = self.countdown - (time.time() - start_time)
            sys.stdout.write(f"\rTime left: {int(time_left)} sec ")
            sys.stdout.flush()
            time.sleep(1)
        if not self.defused:
            ascii_animation(BOMB_WARNING_FRAMES, frame_delay=0.5, repeat=2)
            print("\n" + Colors.RED + "BOOM! The bomb exploded! Mission Failed." + Colors.ENDC)
            os._exit(1)
    
    def attempt_defuse(self, code_input):
        correct_code = "1-4-1"
        if code_input.strip() == correct_code:
            self.defused = True
            return True
        else:
            return False

# Main game engine weaving together the command interface and narrative progression.
class SpyTerminalGame:
    def __init__(self):
        self.fs = FileSystem()
        self.cwd = []  # Current working directory as a list
        self.history = []
        self.bomb = None
        self.game_over = False
        # Track narrative milestones
        self.story_state = {
            "mission_started": False,
            "intel_acquired": False,
            "bomb_engaged": False
        }
    
    def prompt(self):
        prompt_base = f"{Colors.CYAN}spy@terminal{Colors.ENDC}"
        current_path = "/" + "/".join(self.cwd) if self.cwd else "/"
        return f"{prompt_base}:{Colors.GREEN}{current_path}{Colors.ENDC}$ "
    
    def run(self):
        self.intro_sequence()
        while not self.game_over:
            try:
                user_input = input(self.prompt()).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting SpyTerminal. Stay safe, Agent.")
                break
            if not user_input:
                continue
            self.history.append(user_input)
            self.handle_command(user_input)
    
    def intro_sequence(self):
        os.system('cls' if os.name=='nt' else 'clear')
        ascii_animation(MISSION_START_ANIMATION, frame_delay=0.5, repeat=1)
        animate_text(Colors.HEADER + "Welcome, Agent. You have been entrusted with Operation NIGHTSHADE." + Colors.ENDC)
        animate_text("Your mission: extract the secret intel and neutralize the imminent bomb threat.", delay=0.03)
        animate_text("Type 'help' for your command list. Pay close attention to file contents and logs for vital clues.\n", delay=0.03)
    
    def handle_command(self, command_line):
        commands = command_line.split("|")
        for cmd in commands:
            self.execute_command(cmd.strip())
    
    def execute_command(self, cmd):
        parts = cmd.split()
        if not parts:
            return
        command = parts[0]
        args = parts[1:]
        
        if command == "help":
            self.cmd_help()
        elif command == "ls":
            self.cmd_ls(args)
        elif command == "cd":
            self.cmd_cd(args)
        elif command == "cat":
            self.cmd_cat(args)
        elif command == "grep":
            self.cmd_grep(args)
        elif command == "history":
            self.cmd_history()
        elif command == "arm_bomb":
            self.cmd_arm_bomb()
        elif command == "defuse":
            self.cmd_defuse(args)
        elif command == "story":
            self.cmd_story()
        elif command == "exit":
            print("Goodbye, Agent. Stay vigilant!")
            self.game_over = True
        else:
            self.unknown_command(cmd)
    
    def cmd_help(self):
        print("Commands:")
        print("  ls                    : List directories and files.")
        print("  cd [dir]              : Change directory (use '..' to go up).")
        print("  cat [file]            : Read a file's contents.")
        print("  grep [pattern] [file] : Search for a pattern in a file.")
        print("  history               : Display command history.")
        print("  arm_bomb              : Activate the bomb module (only in bomb_module).")
        print("  defuse [code]         : Attempt to defuse the bomb (enter code, e.g., 'defuse 1-4-1').")
        print("  story                 : Show mission status and clues.")
        print("  exit                  : Quit the game.")
    
    def cmd_ls(self, args):
        node = self.fs.get_node(self.cwd)
        if node and node.type == "dir":
            for child in node.children.values():
                if child.type == "dir":
                    print(f"{Colors.BLUE}{child.name}{Colors.ENDC}/", end="  ")
                else:
                    print(child.name, end="  ")
            print()
        else:
            print("Directory not found.")
    
    def cmd_cd(self, args):
        if not args:
            print("Usage: cd [directory]")
            return
        target = args[0]
        if target == "..":
            if self.cwd:
                self.cwd.pop()
            else:
                print("Already at root directory.")
            return
        new_path = self.cwd + [target]
        node = self.fs.get_node(new_path)
        if node and node.type == "dir":
            self.cwd.append(target)
            self.check_story_progress(new_path)
        else:
            print(f"No such directory: {target}")
    
    def cmd_cat(self, args):
        if not args:
            print("Usage: cat [filename]")
            return
        filename = args[0]
        node = self.fs.get_node(self.cwd + [filename])
        if node and node.type == "file":
            print(node.content)
            # Narrative progression from intel file
            if filename == "classified.txt" and not self.story_state["intel_acquired"]:
                animate_text(Colors.HEADER + "\nIntel acquired: The disarm code is hidden in our history. Review logs and use your intuition." + Colors.ENDC)
                self.story_state["intel_acquired"] = True
        else:
            print(f"No such file: {filename}")
    
    def cmd_grep(self, args):
        if len(args) < 2:
            print("Usage: grep [pattern] [filename]")
            return
        pattern = args[0]
        filename = args[1]
        node = self.fs.get_node(self.cwd + [filename])
        if node and node.type == "file":
            found = False
            for line in node.content.splitlines():
                if pattern in line:
                    print(line)
                    found = True
            if not found:
                print("No matches found.")
        else:
            print(f"No such file: {filename}")
    
    def cmd_history(self):
        for idx, cmd in enumerate(self.history, 1):
            print(f"{idx}: {cmd}")
    
    def cmd_arm_bomb(self):
        if self.cwd and self.cwd[-1] == "bomb_module":
            if self.bomb is None:
                self.bomb = Bomb(countdown=20 + random.randint(0, 10))
                ascii_animation(BOMB_WARNING_FRAMES, frame_delay=0.3, repeat=1)
                self.bomb.start_countdown()
                self.story_state["bomb_engaged"] = True
            else:
                print("Bomb already armed!")
        else:
            print("You can only arm the bomb within the 'bomb_module' directory.")
    
    def cmd_defuse(self, args):
        if not self.bomb:
            print("There is no active bomb to defuse!")
            return
        if not args:
            print("Usage: defuse [code]")
            return
        code_attempt = args[0]
        if self.bomb.attempt_defuse(code_attempt):
            animate_text(Colors.GREEN + "\nBomb defused! The enemy plot has been thwarted. Mission accomplished." + Colors.ENDC)
        else:
            print("Incorrect code! Recheck your intel and try again.")
    
    def cmd_story(self):
        print("\n----- Mission Status -----")
        print(f"Mission Brief Read: {'Yes' if self.story_state['mission_started'] else 'No'}")
        print(f"Intel Acquired:    {'Yes' if self.story_state['intel_acquired'] else 'No'}")
        print(f"Bomb Activated:    {'Yes' if self.story_state['bomb_engaged'] else 'No'}")
        print("--------------------------\n")
    
    def unknown_command(self, cmd):
        print(f"Unknown command: '{cmd}'. Try 'help' if you're lost, Agent.")
    
    def check_story_progress(self, new_path):
        joined_path = "/".join(new_path)
        # When entering the missions directory, start the mission
        if joined_path == "missions" and not self.story_state["mission_started"]:
            ascii_animation(MISSION_START_ANIMATION, frame_delay=0.5, repeat=1)
            animate_text(Colors.HEADER + "\nNew Mission: Infiltrate enemy systems, secure classified intel, and neutralize the bomb threat." + Colors.ENDC)
            self.story_state["mission_started"] = True
        # Prompt narrative hints when entering bomb_module
        if joined_path == "bomb_module":
            animate_text(Colors.WARNING + "\nYou are in the Bomb Module. To disable the device, type 'arm_bomb' to begin the sequence." + Colors.ENDC)
    
# Entry point for the game
def main():
    game = SpyTerminalGame()
    game.run()

if __name__ == "__main__":
    main()
