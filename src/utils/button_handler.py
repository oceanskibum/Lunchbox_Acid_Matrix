import RPi.GPIO as GPIO
import time
import json
import os

# 🔘 ButtonHandler: Reads button_config.json and maps GPIO inputs to app functions.
# Supports combos, holds, double-taps, and menu-based layered interactions.

class ButtonHandler:
    def __init__(self, config_path, action_map):
        self.config = self.load_config(config_path)
        self.action_map = action_map
        self.pins = {
            "next": self.config["next"],
            "prev": self.config["prev"]
        }
        self.last_press_time = {}
        self.menu_state = None
        self.menu_timer = None
        self.setup_gpio()

    def load_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for name, pin in self.pins.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.generate_callback(name), bouncetime=200)

    def generate_callback(self, name):
        def callback(channel):
            now = time.time()
            self.last_press_time[name] = now
            self.evaluate_combo(now)
        return callback

    def evaluate_combo(self, now):
        # Check combo timing and map action
        if "modes" in self.config:
            for mode, details in self.config["modes"].items():
                pins = details["combo"]
                if all(pin in self.last_press_time and now - self.last_press_time[pin] < 0.6 for pin in pins):
                    if details["type"] == "tap":
                        self.call_action(mode)
                    elif details["type"] == "hold":
                        time.sleep(details.get("duration", 2))
                        if all(not GPIO.input(self.pins[pin]) for pin in pins):
                            self.call_action(mode)
                    elif details["type"] == "double_tap":
                        self.call_action("enter_menu")
                        self.menu_state = mode
                        self.menu_timer = now
        elif self.menu_state:
            self.handle_menu_logic(now)

    def handle_menu_logic(self, now):
        actions = self.config.get("menu_actions", {}).get(self.menu_state, {})
        timeout = actions.get("timeout", 5)
        if now - self.menu_timer > timeout:
            self.call_action("exit_menu")
            self.menu_state = None
        else:
            if GPIO.input(self.pins[actions.get("increase")]) == 0:
                self.call_action("sensitivity_up")
            elif GPIO.input(self.pins[actions.get("decrease")]) == 0:
                self.call_action("sensitivity_down")

    def call_action(self, action_name):
        if action_name in self.action_map:
            self.action_map[action_name]()

    def check_buttons(self):
        # Periodic check from main loop if needed
        now = time.time()
        self.evaluate_combo(now)
