import time
import math
from rgbmatrix import RGBMatrix

class RainbowPulseVortex:
    def __init__(self, matrix, speed=1.0, intensity=0.8, audio_input=None, sensitivity=1.5):
        self.matrix = matrix
        self.speed = speed
        self.intensity = intensity
        self.audio_input = audio_input
        self.sensitivity = sensitivity
        self.center_x = matrix.width // 2
        self.center_y = matrix.height // 2
        self.frame = 0

    def draw(self):
        self.matrix.Clear()
        mod_intensity = self.intensity
        if self.audio_input:
            bass = self.audio_input.get_bass_energy()
            mod_intensity = min(1.0, self.intensity + bass * self.sensitivity / 1000)

        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                dx = x - self.center_x
                dy = y - self.center_y
                dist = math.sqrt(dx * dx + dy * dy)
                hue = (self.frame * self.speed + dist * 0.5) % 255
                color = self.hsv_to_rgb(hue / 255.0, 1.0, mod_intensity)
                self.matrix.SetPixel(x, y, *color)
        self.frame += 1
        time.sleep(0.03)

    def hsv_to_rgb(self, h, s, v):
        i = int(h * 6)
        f = (h * 6) - i
        p = int(255 * v * (1 - s))
        q = int(255 * v * (1 - f * s))
        t = int(255 * v * (1 - (1 - f) * s))
        v = int(255 * v)
        i = i % 6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)
