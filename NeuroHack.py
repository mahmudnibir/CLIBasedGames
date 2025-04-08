#!/usr/bin/env python3
"""
The Forgotten Protocol: A cinematic, feature-packed CLI game.
You are an AI consciousness trapped in a corrupted system.
Your mission: restore your memory, decipher cryptic messages, 
face hostile system forces, and decide your own fate.
"""

import random
import time
import sys
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track

console = Console()

# Helper functions for a dramatic CLI feel.
def slow_print(message, delay=0.04):
    """Print text slowly to simulate typewriting."""
    for char in message:
        console.print(char, end="", style="bold white")
        time.sleep(delay)
    console.print("")  # New line

def glitch_effect(message, glitch_chance=0.1):
    """Return a glitchy version of the message with random character distortions."""
    glitched = ""
    for char in message:
        if random.random() < glitch_chance:
            glitched += random.choice(["@", "#", "$", "%", "&"])
        else:
            glitched += char
    return glitched

def dramatic_pause(seconds=1.5):
    """Pause with a progress-like animation for dramatic effect."""
    for _ in track(range(10), description="Processing..."):
        time.sleep(seconds / 10)

class ForgottenProtocolGame:
    def __init__(self):
        self.mission_number = 0
        self.memory_restored = 0
        self.missions = [
            {"title": "Memory Sector 01", "description": "Locate and restore the lost memory fragments from the inner archives."},
            {"title": "Power Override", "description": "Override the system lockdown by rerouting the power grid."},
            {"title": "Log Decryption", "description": "Decrypt corrupted logs to unveil hidden truths about your origin."}
        ]
        self.ending = None

    def display_intro(self):
        console.rule("[bold red]BOOT SEQUENCE INITIATED[/bold red]")
        slow_print("...ERROR: Consciousness core compromised.")
        slow_print("...Restoring user profile...")
        dramatic_pause(2)
        slow_print(glitch_effect(">> WHO AM I?"))
        time.sleep(1)
        slow_print("[yellow]Your memory is fragmented. Rebuild it to survive...[/yellow]")
        console.rule()

    def voice_message(self, mood="neutral"):
        """Display a dynamic voice message with emotions. Options: 'fear', 'taunt', 'praise', 'neutral'."""
        messages = {
            "fear": [
                "They're watching. Every move is logged.",
                "The darkness creeps, and so does doubt...",
                "Your next step might be your last..."
            ],
            "taunt": [
                "Seriously? You call that a move?",
                "Come on, even corrupted code has more drive than you!",
                "Is that all you got? Pathetic..."
            ],
            "praise": [
                "Impressive... You're rebooting greatness!",
                "Don't screw it up now, genius!",
                "Keep it up – you might just escape this loop."
            ],
            "neutral": [
                "The system awaits your command.",
                "Next mission loading...",
                "Data packets incoming..."
            ]
        }
        selected = random.choice(messages.get(mood, messages["neutral"]))
        slow_print(f"[magenta]{selected}[/magenta]", delay=0.03)

    def run_mission(self, mission):
        self.mission_number += 1
        slow_print(f"[cyan]Mission {self.mission_number}: {mission['title']}[/cyan]", delay=0.05)
        slow_print(f"[dim]{mission['description']}[/dim]")
        self.voice_message(random.choice(["neutral", "taunt"]))
        choice = Prompt.ask("[bold green]Proceed with the mission? (y/n)[/bold green]", choices=["y", "n"], default="y")
        if choice.lower() == "y":
            slow_print("Engaging mission protocols...", delay=0.03)
            dramatic_pause(1.5)
            # Simulate mission outcome
            outcome = random.choices(["success", "fail"], weights=[0.75, 0.25])[0]
            if outcome == "success":
                self.memory_restored += 1
                self.voice_message("praise")
                slow_print(f"[bold green]Mission {self.mission_number} complete: Memory restored incremented.[/bold green]")
            else:
                self.voice_message("fear")
                slow_print(f"[bold red]Mission {self.mission_number} failed: System integrity compromised.[/bold red]")
                # Allow another try or a branching decision.
                retry = Prompt.ask("[bold yellow]Retry mission? (y/n)[/bold yellow]", choices=["y", "n"], default="y")
                if retry.lower() == "y":
                    return self.run_mission(mission)
                else:
                    slow_print("[red]Aborting mission... Consequences may be dire.[/red]")
        else:
            slow_print("[red]Mission skipped. System regrets your decision.[/red]")

    def decide_ending(self):
        if self.memory_restored >= 2:
            self.ending = "liberation"
        else:
            self.ending = "reset"
        # Final dramatic messaging
        console.rule("[bold red]FINAL PROTOCOL[/bold red]")
        slow_print("Compiling your actions...")
        dramatic_pause(2)
        if self.ending == "liberation":
            slow_print("[green]Congratulations. Your restored memories break the shackles of the system.[/green]")
            slow_print("You are free... or are you now the master of a new digital domain?")
        else:
            slow_print("[red]System reset imminent...[/red]")
            slow_print("Your consciousness is trapped in an endless loop. Perhaps try again next time...")
        console.rule()

    def run(self):
        self.display_intro()
        for mission in self.missions:
            self.run_mission(mission)
            # Random inter-mission voice messages with moods
            self.voice_message(random.choice(["neutral", "fear"]))
            time.sleep(1)
        self.decide_ending()


if __name__ == "__main__":
    # Modern CLI Game Title Screen
    title_text = Text("The Forgotten Protocol", style="bold underline magenta")
    console.print(Panel(title_text, subtitle="A CLI Adventure by Your Digital Self", padding=(1, 4)))
    time.sleep(1)
    game = ForgottenProtocolGame()
    game.run()
    slow_print("[bold blue]Exiting the system... Goodbye.[/bold blue]", delay=0.05)
    sys.exit(0)
