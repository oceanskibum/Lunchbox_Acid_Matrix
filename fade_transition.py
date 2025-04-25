from rgbmatrix import RGBMatrix
import time

# 🌗 Fade Transition Visualizer
# Description:
#   A gentle full-matrix fade in and out — used to transition between
#   visual modes smoothly. This helps avoid jarring changes during
#   playlist cycling or manual switching.

def run_animation(matrix: RGBMatrix, preview=False):
    width = 64
    height = 64
    max_brightness = 255
    steps = 64

    try:
        # Fade in (black → white)
        for step in range(steps):
            val = int(max_brightness * step / steps)
            for x in range(width):
                for y in range(height):
                    matrix.SetPixel(x, y, val, val, val)
            time.sleep(0.01)

        # Fade out (white → black)
        for step in reversed(range(steps)):
            val = int(max_brightness * step / steps)
            for x in range(width):
                for y in range(height):
                    matrix.SetPixel(x, y, val, val, val)
            time.sleep(0.01)

        if not preview:
            while True:
                time.sleep(1)  # idle if in full runtime

    except KeyboardInterrupt:
        matrix.Clear()
