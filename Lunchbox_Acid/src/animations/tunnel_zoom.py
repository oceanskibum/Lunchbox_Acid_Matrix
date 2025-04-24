
import time
import math
from rgbmatrix import RGBMatrix

class TunnelZoom:
    def __init__(self, matrix, zoom_speed=0.6, line_count=12, audio_input=None, sensitivity=1.5):
        self.matrix = matrix
        self.zoom_speed = zoom_speed
        self.line_count = line_count
        self.audio_input = audio_input
        self.sensitivity = sensitivity
        self.frame = 0

    def draw(self):
        self.matrix.Clear()
        center_x = self.matrix.width // 2
        center_y = self.matrix.height // 2
        angle_step = 2 * math.pi / self.line_count
        depth = self.frame * self.zoom_speed

        for i in range(self.line_count):
            angle = i * angle_step + depth * 0.05
            for d in range(8, 32):
                x = int(center_x + d * math.cos(angle))
                y = int(center_y + d * math.sin(angle))
                if 0 <= x < self.matrix.width and 0 <= y < self.matrix.height:

        mod = 1.0
        if self.audio_input:
            bass = self.audio_input.get_bass_energy()
            mod = min(2.0, 1.0 + bass * self.sensitivity / 1000)
                    int((255 - (d / 32) * 255) * mod)
                    r = (brightness * (i % 3 == 0))
                    g = (brightness * (i % 3 == 1))
                    b = (brightness * (i % 3 == 2))
                    self.matrix.SetPixel(x, y, int(r), int(g), int(b))

        self.frame += 1
        time.sleep(0.03)

# Suggestions:
# - Higher zoom_speed increases the tunnel movement
# - More line_count creates tighter "warp tunnel" lines
