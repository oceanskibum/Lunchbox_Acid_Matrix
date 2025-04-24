# USB Microphone Input + Sensitivity + Beat Detection

import sounddevice as sd
import numpy as np

class AudioInput:
    def __init__(self, sensitivity=1.5):
        self.sensitivity = sensitivity
        self.stream = None
        self.callback = None

    def start(self, callback):
        self.callback = callback
        self.stream = sd.InputStream(callback=self.process, channels=1, samplerate=44100)
        self.stream.start()

    def process(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * self.sensitivity
        if self.callback:
            self.callback(volume_norm)
