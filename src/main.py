#!/usr/bin/env python3
import json
import os
import time
from src.animations import ANIMATION_MODES

CONFIG_PATH = "config/config.json"

ascii_art = """
 _                      _     ____                           _     _ 
| |                    | |   |  _ \                /\       (_)   | |
| |    _   _ _ __   ___| |__ | |_) | _____  __    /  \   ___ _  __| |
| |   | | | | '_ \ / __| '_ \|  _ < / _ \ \/ /   / /\ \ / __| |/ _` |
| |___| |_| | | | | (__| | | | |_) | (_) >  <   / ____ \ (__| | (_| |
|______\__,_|_| |_|\___|_| |_|____/ \___/_/\_\ /_/    \_\___|_|\__,_|

>>> SYSTEM ONLINE — WELCOME TO LUNCHBOX_ACID_MATRIX CLI
>>> V1.13
"""

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print("\nSettings saved to config/config.json")

def prompt_bool(label, current):
    prompt = f"{label}? [Y/n] (currently: {'Enabled' if current else 'Disabled'}): "
    choice = input(prompt).strip().lower()
    if choice in ["y", "yes", ""]:
        return True
    elif choice in ["n", "no"]:
        return False
    else:
        print("Invalid input. Please enter Y or N.")
        return prompt_bool(label, current)

def prompt_float(label, current, min_val=0.1, max_val=5.0):
    try:
        val = float(input(f"{label} (current: {current}) [Range: {min_val}–{max_val}]: ").strip())
        return max(min(val, max_val), min_val)
    except ValueError:
        print("Invalid input. Enter a number.")
        return prompt_float(label, current, min_val, max_val)

def prompt_int(label, current, min_val=0, max_val=100):
    try:
        val = int(input(f"{label} (current: {current}) [Range: {min_val}–{max_val}]: ").strip())
        return max(min(val, max_val), min_val)
    except ValueError:
        print("Invalid input. Enter an integer.")
        return prompt_int(label, current, min_val, max_val)

def run_live_preview(mode):
    print(f"Running preview for {mode}...")
    import importlib
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.slowdown_gpio = 4
    options.pwm_bits = 11
    options.gpio_mapping = 'adafruit-hat-pwm'
    options.hardware_pulsing = False

    matrix = RGBMatrix(options=options)
    try:
        module = importlib.import_module(f"src.animations.{mode}")
        module.run_animation(matrix, preview=True)
    except Exception as e:
        print(f" Error: {e}")
    finally:
        matrix.Clear()
        print("Preview ended.")

def show_menu(config):
    print("\n=== 🎛 Lunchbox Acid Matrix Configurator ===")
    print(f"[1] Select Visual Mode              [Current: {config['visualization']}]")
    print(f"[2] Adjust Brightness              [Current: {config['brightness']}]")
    print(f"[3] Enable/Disable Audio-Reactive  [Current: {'Enabled' if config['audio_reactive'] else 'Disabled'}]")
    print(f"[4] Adjust Mic Sensitivity         [Current: {config['audio_sensitivity']}]")
    print(f"[5] Enable/Disable Motion (IMU)    [Current: {'Enabled' if config['motion_mode_enabled'] else 'Disabled'}]")
    print(f"[6] Toggle Playlist Mode           [Current: {'Enabled' if config['playlist_mode'] else 'Disabled'}]")
    print(f"[7] View Animation Mode Index")
    print(f"[8] Run Live Matrix Preview")
    print(f"[9] Save Settings & Exit")
    print(f"[0] Exit without Saving")
    print("============================================")

def run_cli():
    config = load_config()
    while True:
        show_menu(config)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("Available modes:")
            for mode in ANIMATION_MODES:
                print(f"  - {mode}")
            selected = input("Type a mode name to select: ").strip()
            if selected in ANIMATION_MODES:
                config["visualization"] = selected
                if prompt_bool("Run preview for this mode", True):
                    run_live_preview(selected)
            else:
                print("Invalid mode.")
        elif choice == "2":
            config["brightness"] = prompt_int("Set brightness level", config["brightness"])
        elif choice == "3":
            config["audio_reactive"] = prompt_bool("Enable Audio-Reactive mode", config["audio_reactive"])
        elif choice == "4":
            config["audio_sensitivity"] = prompt_float("Set mic sensitivity", config["audio_sensitivity"])
        elif choice == "5":
            config["motion_mode_enabled"] = prompt_bool("Enable motion-reactive dancer mode", config["motion_mode_enabled"])
        elif choice == "6":
            config["playlist_mode"] = prompt_bool("Enable Playlist Mode", config["playlist_mode"])
        elif choice == "7":
            print("\n🗂 Available Modes:")
            for mode in ANIMATION_MODES:
                print(f"  - {mode}")
        elif choice == "8":
            run_live_preview(config["visualization"])
        elif choice == "9":
            save_config(config)
            break
        elif choice == "0":
            print("Exited without saving.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    run_cli()
