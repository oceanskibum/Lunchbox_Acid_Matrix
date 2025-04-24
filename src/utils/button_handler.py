import time
import json
import RPi.GPIO as GPIO

class ButtonHandler:
    def __init__(self, config_path, callbacks):
        self.load_config(config_path)
        self.callbacks = callbacks
        self.state = {"mode": None, "last_press": 0, "last_combo": 0, "menu_entered": 0}
        self.mode_start_time = None

        GPIO.setmode(GPIO.BCM)
        for name, pin in self.buttons.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def load_config(self, path):
        with open(path) as f:
            config = json.load(f)
        self.buttons = {name: config[name] for name in ["next", "prev"]}
        self.modes = config.get("modes", {})
        self.menu_actions = config.get("menu_actions", {})

    def check_buttons(self):
        now = time.time()
        pressed = {name: not GPIO.input(pin) for name, pin in self.buttons.items()}

        if self.state["mode"]:
            # Handle menu actions
            for menu, act in self.menu_actions.items():
                if self.state["mode"] == act["mode"]:
                    if pressed[act["increase"]]:
                        self.callbacks.get("sensitivity_up", lambda: None)()
                        self.state["last_press"] = now
                    elif pressed[act["decrease"]]:
                        self.callbacks.get("sensitivity_down", lambda: None)()
                        self.state["last_press"] = now
                    # Timeout
                    if now - self.state["last_press"] > act.get("timeout", 5):
                        self.state["mode"] = None
                        self.callbacks.get("exit_menu", lambda: None)()
            return

        # Check for combo press
        if all(pressed.values()):
            if now - self.state["last_combo"] < 1.5:
                mode = [k for k, v in self.modes.items() if v["type"] == "double_tap"]
                if mode:
                    self.state["mode"] = mode[0]
                    self.state["last_press"] = now
                    self.callbacks.get("enter_menu", lambda: None)()
                    return
            self.state["last_combo"] = now

        # Check hold actions
        for mode, action in self.modes.items():
            if action["type"] == "hold":
                if all(pressed[b] for b in action["combo"]):
                    if now - self.state["last_press"] > action.get("duration", 2):
                        self.callbacks.get(mode, lambda: None)()
                        self.state["last_press"] = now
                        return

        # Check tap actions
        if any(pressed.values()):
            for mode, action in self.modes.items():
                if action["type"] == "tap":
                    if all(pressed[b] for b in action["combo"]):
                        self.callbacks.get(mode, lambda: None)()
                        self.state["last_press"] = now
                        return
