
import math
import time
from rgbmatrix import RGBMatrix

class PlasmaCloud:
    def __init__(self, matrix, movement_speed=0.4, color_shift=True, audio_input=None, sensitivity=1.5):
        self.matrix = matrix
        self.audio_input = audio_input
        self.sensitivity = sensitivity
        self.frame = 0
        self.movement_speed = movement_speed
        self.color_shift = color_shift

    def draw(self):
        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                v = math.sin(x * 0.13 + self.frame * self.movement_speed)
                v += math.sin((y * 0.17 + self.frame * self.movement_speed) / 2)
                v += math.sin((x + y) * 0.11 + self.frame * self.movement_speed)

        mod = 1.0
        if self.audio_input:
            bass = self.audio_input.get_bass_energy()
            mod = min(2.0, 1.0 + bass * self.sensitivity / 1000)
                v = v / 3.0 * mod
                hue = (v + 1) * 128
                color = self.hsv_to_rgb((hue % 255) / 255.0, 1.0, 1.0 if self.color_shift else 0.8)
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

# Suggestions:
# - Higher movement_speed = more intense motion
# - Set color_shift to False for a calmer effect
