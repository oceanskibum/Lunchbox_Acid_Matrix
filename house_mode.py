from rgbmatrix import RGBMatrix
import time
import math

# 🎛 House Mode Visualizer
# Description:
#   This animation creates slow, pulsing sine wave patterns
#   that move across the matrix to mimic minimal house beats.
#   Soft color gradients create a flowing, club-like vibe.

def run_animation(matrix: RGBMatrix, preview=False):
    width = 64
    height = 64
    t = 0  # Time offset for animation

    try:
        while True:
            matrix.Clear()
            for x in range(width):
                # Use sine wave + time offset to animate vertical shift
                y_offset = int((math.sin((x + t) * 0.2) + 1) * (height // 2 - 1))
                # Color shift using hue gradient
                r = int((math.sin(t * 0.1 + x * 0.1) + 1) * 127)
                g = int((math.sin(t * 0.1 + x * 0.1 + 2) + 1) * 127)
                b = int((math.sin(t * 0.1 + x * 0.1 + 4) + 1) * 127)

                for y in range(y_offset - 2, y_offset + 3):  # Draw a vertical "pulse"
                    if 0 <= y < height:
                        matrix.SetPixel(x, y, r, g, b)

            time.sleep(0.04)  # ~25 FPS
            t += 1

            if preview and t > 250:
                break
    except KeyboardInterrupt:
        matrix.Clear()
