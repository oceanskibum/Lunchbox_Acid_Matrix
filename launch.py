#!/usr/bin/env python3
import json
import time
import importlib
import RPi.GPIO as GPIO
import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# GPIO Pins
NEXT_BUTTON = 17  # Pin 11
PREV_BUTTON = 27  # Pin 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(NEXT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PREV_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Load configs and state
with open("config/config.json") as f:
    config = json.load(f)

state_path = "config/state.json"
if os.path.exists(state_path):
    with open(state_path) as f:
        state = json.load(f)
else:
    state = {"brightness": 80, "last_effect": config["visualization"], "last_interaction": time.time()}

effects_list = list(config["effects"].keys())
current_index = effects_list.index(state.get("last_effect", config["visualization"]))

# Setup matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.pwm_bits = 11
options.gpio_slowdown = 4

matrix = RGBMatrix(options=options)
matrix.brightness = state["brightness"]

def load_animation(index):
    selected = effects_list[index]
    params = config["effects"][selected]
    module_path = f"src.animations.{selected}"
    class_name = ''.join([part.capitalize() for part in selected.split('_')])
    animation_module = importlib.import_module(module_path)
    animation_class = getattr(animation_module, class_name)
    return animation_class(matrix, **params), selected

def save_state():
    with open(state_path, "w") as f:
        state["last_effect"] = effects_list[current_index]
        state["brightness"] = matrix.brightness
        state["last_interaction"] = time.time()
        json.dump(state, f, indent=2)

def display_idle_message(message="404 - Vibes Not Found"):
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("rpi-rgb-led-matrix/fonts/6x10.bdf")
    color = graphics.Color(255, 0, 0)
    pos = offscreen_canvas.width
    while True:
        offscreen_canvas.Clear()
        len_msg = graphics.DrawText(offscreen_canvas, font, pos, 32, color, message)
        pos -= 1
        if pos + len_msg < 0:
            pos = offscreen_canvas.width
        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

# Animation setup
effect, current_name = load_animation(current_index)
last_button_time = time.time()
brightness_levels = [20, 40, 60, 80, 100]
brightness_index = brightness_levels.index(matrix.brightness) if matrix.brightness in brightness_levels else 3

try:
    while True:
        now = time.time()

        # Run current effect
        effect.draw()

        # Overheat protection
        with open("/sys/class/thermal/thermal_zone0/temp") as tf:
            temp = int(tf.read()) / 1000
        if temp > 75:
            matrix.brightness = 40
            continue

        # Idle detection
        if now - state.get("last_interaction", now) > 600:
            display_idle_message(config.get("idle_message", "404 - Vibes Not Found"))

        # Auto-dim
        if now - state.get("last_interaction", now) > 300:
            matrix.brightness = 20

        # Buttons
        next_pressed = not GPIO.input(NEXT_BUTTON)
        prev_pressed = not GPIO.input(PREV_BUTTON)

        if next_pressed and prev_pressed:
            hold_start = now
            while not GPIO.input(NEXT_BUTTON) and not GPIO.input(PREV_BUTTON):
                if time.time() - hold_start > 2:
                    save_state()
                    os.system("sudo shutdown now")
            brightness_index = (brightness_index + 1) % len(brightness_levels)
            matrix.brightness = brightness_levels[brightness_index]
            state["last_interaction"] = now
            time.sleep(0.3)

        elif next_pressed:
            hold_start = now
            while not GPIO.input(NEXT_BUTTON):
                if config.get("ota_enabled", False) and time.time() - hold_start > 10:
                    os.system("git pull")
                    time.sleep(2)
            current_index = (current_index + 1) % len(effects_list)
            effect, current_name = load_animation(current_index)
            state["last_interaction"] = now
            time.sleep(0.3)

        elif prev_pressed:
            current_index = (current_index - 1) % len(effects_list)
            effect, current_name = load_animation(current_index)
            state["last_interaction"] = now
            time.sleep(0.3)

        save_state()

except KeyboardInterrupt:
    GPIO.cleanup()
    save_state()
