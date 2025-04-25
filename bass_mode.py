from rgbmatrix import RGBMatrix
import time
import random

# 🔊 Bass Mode Visualizer
# Description:
#   This mode simulates intense bass drops with chaotic strobes
#   and quick pulses across the matrix. It uses randomized bursts
#   and flashing bands for a high-energy, bass-heavy vibe.

def run_animation(matrix: RGBMatrix, preview=False):
    width = 64
    height = 64
    pulse_timer = 0

    try:
        while True:
            matrix.Clear()

            # Random horizontal strobe band
            if pulse_timer % 5 == 0:
                y_band = random.randint(0, height - 1)
                r = random.randint(128, 255)
                g = random.randint(0, 50)
                b = random.randint(128, 255)
                for x in range(width):
                    for y_offset in range(-2, 3):
                        y = y_band + y_offset
                        if 0 <= y < height:
                            matrix.SetPixel(x, y, r, g, b)

            # Random dot scatter
            for _ in range(100):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                matrix.SetPixel(x, y, random.randint(0, 255), 0, random.randint(100, 255))

            time.sleep(0.03)  # Faster refresh for strobe effect
            pulse_timer += 1

            if preview and pulse_timer > 200:
                break

    except KeyboardInterrupt:
        matrix.Clear()
