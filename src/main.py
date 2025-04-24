#!/usr/bin/env python3
import json
import time
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")

ascii_art = """
   _                _              _           _             _    _             
  | |              | |            | |         | |           | |  (_)            
  | |     ___  __ _| | _____   ___| |__   __ _| |_   _  __ _| | ___ _ __   __ _ 
  | |    / _ \/ _` | |/ / _ \ / __| '_ \ / _` | | | | |/ _` | |/ / | '_ \ / _` |
  | |___|  __/ (_| |   < (_) | (__| | | | (_| | | |_| | (_| |   <| | | | | (_| |
  \_____/\___|\__,_|_|\_\___/ \___|_| |_|\__,_|_|\__,_|\__,_|_|\_\_|_| |_|\__, |
                                                                           __/ |
                                                                          |___/ 
"""

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print("\n✅ Config saved successfully!")
    time.sleep(1)

def spinner(msg="Saving..."):
    print(msg, end="")
    for _ in range(6):
        for c in "|/-\\": print(f"\b{c}", end="", flush=True); time.sleep(0.1)
    print("\b ✔")

def show_menu():
    os.system("clear" if os.name == "posix" else "cls")
    print(ascii_art)
    print("🎛  Lunchbox Acid Matrix: Configuration CLI Tool")
    print("-------------------------------------------------")
    print("1. Set Visualization Mode")
    print("2. Toggle Audio Reactive")
    print("3. Adjust Audio Sensitivity")
    print("4. Toggle Motion (Dancer Mode)")
    print("5. Set Brightness")
    print("6. Toggle Playlist Mode")
    print("7. Save & Exit")
    print("0. Exit without Saving")
    print("-------------------------------------------------")

def run_cli():
    config = load_config()
    while True:
        show_menu()
        print(f"Current Mode: {config['visualization']}")
        print(f"Audio Reactive: {config['audio_reactive']}  | Sensitivity: {config['audio_sensitivity']}")
        print(f"Motion: {config['motion_mode_enabled']}  | Brightness: {config['brightness']}")
        print(f"Playlist: {config['playlist_mode']}")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            val = input("Enter visualization mode [house_mode, bass_mode, techno_mode, basshouse_mode, dancer_mode, idle_mode]: ").strip()
            config["visualization"] = val
        elif choice == "2":
            config["audio_reactive"] = not config["audio_reactive"]
        elif choice == "3":
            try:
                val = float(input("Enter sensitivity (e.g., 1.0 - 3.0): "))
                config["audio_sensitivity"] = val
            except ValueError:
                print("❌ Invalid input.")
        elif choice == "4":
            config["motion_mode_enabled"] = not config["motion_mode_enabled"]
        elif choice == "5":
            try:
                val = int(input("Set brightness (0–100): "))
                config["brightness"] = max(0, min(100, val))
            except ValueError:
                print("❌ Invalid input.")
        elif choice == "6":
            config["playlist_mode"] = not config["playlist_mode"]
        elif choice == "7":
            spinner("💾 Saving")
            save_config(config)
            break
        elif choice == "0":
            print("Exited without saving.")
            break
        else:
            print("❌ Invalid option.")
        input("\nPress ENTER to continue...")

if __name__ == "__main__":
    run_cli()
