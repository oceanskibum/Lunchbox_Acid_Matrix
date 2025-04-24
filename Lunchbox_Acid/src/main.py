#!/usr/bin/env python3
import time
import sys
import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"

ASCII_HEADER = r"""
  _                 _               _               _    _           _       
 | |               | |             | |             | |  (_)         | |      
 | |     ___   ___ | | _____  _   _| |__   ___ _ __ | | ___  ___  ___| |_ ___ 
 | |    / _ \ / _ \| |/ / _ \| | | | '_ \ / _ \ '_ \| |/ / |/ _ \/ __| __/ __|
 | |___| (_) | (_) |   < (_) | |_| | |_) |  __/ | | |   <| |  __/ (__| |_\__ \
 |______\___/ \___/|_|\_\___/ \__,_|_.__/ \___|_| |_|_|\_\_|\___|\___|\__|___/
                                                                             
"""

def loading_bar(text="Loading", duration=2.5, bar_length=30):
    print(f"\n{text}")
    for i in range(bar_length + 1):
        percent = int((i / bar_length) * 100)
        bar = "=" * i + "-" * (bar_length - i)
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / bar_length)
    print("\n")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def main_menu():
    os.system("clear")
    print(ASCII_HEADER)
    print("Welcome to Lunchbox Acid Viz!")
    print("Select a visualization preset to start:\n")

    config = load_config()
    effects = list(config["effects"].keys())

    for i, effect in enumerate(effects, 1):
        print(f" {i}. {effect.replace('_', ' ').title()}")

    print(" q. Quit\n")
    choice = input("Enter your choice: ")

    if choice.lower() == 'q':
        print("Goodbye!")
        sys.exit(0)

    try:
        idx = int(choice) - 1
        selected = effects[idx]
        print(f"\nLaunching: {selected.replace('_', ' ').title()}...")
        loading_bar("Launching Visualizer")
        # Placeholder for actual launch
        print(f"[Simulated] Running {selected} with config:")
        print(json.dumps(config["effects"][selected], indent=2))
    except (ValueError, IndexError):
        print("Invalid choice. Try again.")
        time.sleep(1)
        main_menu()

if __name__ == "__main__":
    main_menu()
