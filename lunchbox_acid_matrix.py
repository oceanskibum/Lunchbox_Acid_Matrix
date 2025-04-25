#!/usr/bin/env python3
import sys, os
import json
import time
import importlib

# Ensure src/ is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from rgbmatrix import RGBMatrix, RGBMatrixOptions

CONFIG_PATH = "config/config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def setup_matrix():
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.gpio_slowdown = 4  # Renamed from slowdown_gpio
    options.pwm_bits = 11
    options.hardware_mapping = 'adafruit-hat-pwm'  # Replaces gpio_mapping
    options.disable_hardware_pulsing = True  # Replaces hardware_pulsing
    return RGBMatrix(options=options)

def run_visualization(matrix, mode_name):
    try:
        module = importlib.import_module(f"animations.{mode_name}")
        if hasattr(module, "run_animation"):
            module.run_animation(matrix, preview=False)
        else:
            print(f"❌ Mode '{mode_name}' does not implement run_animation().")
    except Exception as e:
        print(f"💥 Failed to run mode '{mode_name}': {e}")
        matrix.Clear()

def main():
    print("🚀 Launching Lunchbox Acid Matrix Runtime")
    config = load_config()
    matrix = setup_matrix()
    selected_mode = config.get("visualization", "house_mode")
    print(f"🎨 Mode selected: {selected_mode}")
    run_visualization(matrix, selected_mode)

if __name__ == "__main__":
    main()
