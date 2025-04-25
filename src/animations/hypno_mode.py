from rgbmatrix import RGBMatrix
import math
import time

# 🌀 Hypno Mode Visualizer
# Description:
#   Spinning black and white spiral, classic hypnosis style.
#   Smooth trippy rotation effect ideal for visual immersion.

def run_animation(matrix: RGBMatrix, preview=False):
    width = 64
    height = 64
    center_x = width // 2
    center_y = height // 2
    t = 0

    try:
        while True:
            matrix.Clear()

            for x in range(width):
                for y in range(height):
                    dx = x - center_x
                    dy = y - center_y
                    distance = math.sqrt(dx * dx + dy * dy)
                    angle = math.atan2(dy, dx) + t * 0.15
                    band = int((angle + distance * 0.2) * 3) % 2
                    color = (255, 255, 255) if band == 0 else (0, 0, 0)
                    matrix.SetPixel(x, y, *color)

            time.sleep(0.04)
            t += 1

            if preview and t > 150:
                break

    except KeyboardInterrupt:
        matrix.Clear()
