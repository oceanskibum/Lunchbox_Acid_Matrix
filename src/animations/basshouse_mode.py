from rgbmatrix import RGBMatrix
import time
import math
import random

# 🧬 Basshouse Mode Visualizer
# Description:
#   Combines elements of bass-mode's glitchiness with the
#   flowing structure of house. Result: rhythmic chaos with form.

def run_animation(matrix: RGBMatrix, preview=False):
    width = 64
    height = 64
    t = 0

    try:
        while True:
            matrix.Clear()

            # Smooth sinusoidal wave (house style)
            for x in range(width):
                y = int((math.sin((x + t) * 0.15) + 1) * (height / 2 - 1))
                r = int((math.sin(t * 0.1 + x * 0.05) + 1) * 127)
                g = 0
                b = 255 - r
                for offset in range(-1, 2):
                    if 0 <= y + offset < height:
                        matrix.SetPixel(x, y + offset, r, g, b)

            # Glitch scatter overlay (bass element)
            for _ in range(15):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                matrix.SetPixel(x, y, random.randint(150, 255), random.randint(0, 50), random.randint(100, 255))

            time.sleep(0.04)
            t += 1

            if preview and t > 250:
                break

    except KeyboardInterrupt:
        matrix.Clear()
