#!/usr/bin/env python3
import json
import time
import threading
import os

from src.utils.button_handler import ButtonHandler
from src.audio.audio_input import AudioInput
from src.input.imu_input import IMUInput

CONFIG_PATH = "config/config.json"
STATE_PATH = "config/state.json"
PLAYLIST_PATH = "config/playlist.json"

def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)

def fake_visualizer(mode):
    print(f"🎨 [Mode Active]: {mode}")
    print("✨ Animating on matrix...
")

class Runtime:
    def __init__(self):
        self.config = load_config(CONFIG_PATH)
        self.state = load_config(STATE_PATH)
        self.playlist = load_config(PLAYLIST_PATH)["default"]
        self.playlist_index = 0
        self.mode = self.config["visualization"]
        self.audio = AudioInput(sensitivity=self.config["audio_sensitivity"]) if self.config["audio_reactive"] else None
        self.imu = IMUInput() if self.config["motion_mode_enabled"] else None
        self.running = True
        self.button_handler = ButtonHandler("config/button_config.json", {
            "brightness_toggle": self.brightness_toggle,
            "shutdown": self.shutdown,
            "enter_menu": lambda: print("🎚 Entering sensitivity menu"),
            "sensitivity_up": self.sensitivity_up,
            "sensitivity_down": self.sensitivity_down,
            "exit_menu": lambda: print("Exiting menu")
        })

    def brightness_toggle(self):
        self.config["brightness"] = 100 if self.config["brightness"] < 50 else 25
        print(f"🔆 Brightness set to {self.config['brightness']}")

    def sensitivity_up(self):
        self.config["audio_sensitivity"] += 0.2
        print(f"🔊 Sensitivity: {self.config['audio_sensitivity']:.2f}")

    def sensitivity_down(self):
        self.config["audio_sensitivity"] = max(0.2, self.config["audio_sensitivity"] - 0.2)
        print(f"🔉 Sensitivity: {self.config['audio_sensitivity']:.2f}")

    def playlist_loop(self):
        while self.running:
            self.mode = self.playlist[self.playlist_index]
            fake_visualizer(self.mode)
            self.playlist_index = (self.playlist_index + 1) % len(self.playlist)
            time.sleep(90)

    def audio_loop(self):
        self.audio.start(lambda volume: print(f"🎧 Volume={volume:.2f}") if volume > 30 else None)

    def motion_loop(self):
        while self.running:
            mag = self.imu.read_movement()
            if mag > 25000:
                fake_visualizer("dancer_mode")
            time.sleep(1)

    def run(self):
        print("Starting Lunchbox Acid Matrix runtime...")
        threads = []
        if self.config["playlist_mode"]:
            threads.append(threading.Thread(target=self.playlist_loop))
        if self.audio:
            threads.append(threading.Thread(target=self.audio_loop))
        if self.imu:
            threads.append(threading.Thread(target=self.motion_loop))

        for t in threads:
            t.start()

        try:
            while self.running:
                self.button_handler.check_buttons()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
            save_state(self.config)
            print("\n Exited cleanly.")

if __name__ == "__main__":
    Runtime().run()
