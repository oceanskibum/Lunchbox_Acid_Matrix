
import time
import random
from rgbmatrix import RGBMatrix

class CellularAutomata:
    def __init__(self, matrix, seed_density=0.25, color_mode="rainbow", audio_input=None, sensitivity=1.5):
        self.matrix = matrix
        self.grid = [[0 for _ in range(matrix.width)] for _ in range(matrix.height)]
        self.audio_input = audio_input
        self.sensitivity = sensitivity
        self.frame = 0
        self.color_mode = color_mode
        for y in range(matrix.height):
            for x in range(matrix.width):
                self.grid[y][x] = 1 if random.random() < seed_density else 0

    def draw(self):
        new_grid = [[0 for _ in range(self.matrix.width)] for _ in range(self.matrix.height)]
        for y in range(1, self.matrix.height - 1):
            for x in range(1, self.matrix.width - 1):
                neighbors = sum([
                    self.grid[y+dy][x+dx]
                    for dy in [-1, 0, 1]
                    for dx in [-1, 0, 1]
                    if not (dy == 0 and dx == 0)
                ])
                if self.grid[y][x] == 1:
                    new_grid[y][x] = 1 if neighbors in [2, 3] else 0
                else:
                    new_grid[y][x] = 1 if neighbors == 3 else 0

        self.grid = new_grid
        for y in range(self.matrix.height):
            for x in range(self.matrix.width):
                if self.grid[y][x]:

        mod = 1.0
        if self.audio_input:
            bass = self.audio_input.get_bass_energy()
            mod = min(2.0, 1.0 + bass * self.sensitivity / 1000)
                    self.get_color(x, y, mod)
                    self.matrix.SetPixel(x, y, *color)
                else:
                    self.matrix.SetPixel(x, y, 0, 0, 0)

        self.frame += 1
        time.sleep(0.1)

    def get_color(self, x, y):
        # Creates a rainbow color cycle effect based on frame and position
        r = int((math.sin(0.3 * x + self.frame * 0.1) + 1) * 127)
        g = int((math.sin(0.3 * y + self.frame * 0.1 + 2) + 1) * 127)
        b = int((math.sin(0.3 * (x + y) + self.frame * 0.1 + 4) + 1) * 127)
        return (r, g, b)

# Suggestions:
# - seed_density around 0.1 to 0.3 is good for sparse to dense starts
# - set color_mode to 'static' to use one color instead of rainbow
