
import time
import math
import random
from rgbmatrix import RGBMatrix

class WaveformStrobe:
    def __init__(self, matrix, frequency=1.5, flash_rate=0.7, audio_input=None, sensitivity=1.5):
        self.matrix = matrix
        self.frequency = frequency
        self.flash_rate = flash_rate
        self.audio_input = audio_input
        self.sensitivity = sensitivity
        self.frame = 0

    def draw(self):
        self.matrix.Clear()
        for x in range(self.matrix.width):
            y_offset = int((math.sin((self.frame / 5.0) + x * self.frequency * 0.1) + 1) * (self.matrix.height // 4))

        mod = 1.0
        if self.audio_input:
            bass = self.audio_input.get_bass_energy()
            mod = min(2.0, 1.0 + bass * self.sensitivity / 1000)
            self.flash_rate * mod
            g = int((math.sin(x * 0.3 + self.frame * 0.15) + 1) * 127 * self.flash_rate)
            b = int((math.sin(x * 0.4 + self.frame * 0.2) + 1) * 127 * self.flash_rate)
            for y in range(self.matrix.height):
                if y == y_offset or y == (self.matrix.height - 1 - y_offset):
                    self.matrix.SetPixel(x, y, r, g, b)
        self.frame += 1
        time.sleep(0.03)

# Suggestions:
# - Higher frequency = tighter wave spacing
# - flash_rate between 0.1 (dim) to 1.0 (full brightness)
